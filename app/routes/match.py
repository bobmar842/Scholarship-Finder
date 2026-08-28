from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import MatchResult, Resume
from app.services.matching_service import compute_match

match_bp = Blueprint("match", __name__)


@match_bp.post("/")
@jwt_required()
def match():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    resume_id = data.get("resume_id")
    job_description = (data.get("job_description") or "").strip()

    if not resume_id or not job_description:
        return jsonify({"message": "resume_id and job_description are required"}), 400

    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    if not resume:
        return jsonify({"message": "Resume not found"}), 404
    if not resume.extracted_text:
        return jsonify({"message": "Resume has no extractable text"}), 422

    try:
        result = compute_match(resume.extracted_text, job_description)
    except Exception as exc:
        return jsonify({"message": f"Matching failed: {exc}"}), 502

    match_result = MatchResult(
        resume_id=resume.id,
        job_description=job_description,
        match_score=result["match_score"],
        matched_keywords=",".join(result["matched_keywords"]),
        missing_keywords=",".join(result["missing_keywords"]),
    )
    db.session.add(match_result)
    db.session.commit()

    return jsonify(match_result.to_dict()), 201


@match_bp.get("/history/<int:resume_id>")
@jwt_required()
def match_history(resume_id):
    user_id = get_jwt_identity()
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    if not resume:
        return jsonify({"message": "Resume not found"}), 404

    results = (
        MatchResult.query.filter_by(resume_id=resume.id)
        .order_by(MatchResult.created_at.desc())
        .all()
    )
    return jsonify([r.to_dict() for r in results]), 200
