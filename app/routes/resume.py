import io

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Resume
from app.services.cloudinary_service import upload_resume
from app.services.pdf_service import extract_text_from_pdf

resume_bp = Blueprint("resume", __name__)


def _allowed_file(filename: str) -> bool:
    allowed = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@resume_bp.post("/upload")
@jwt_required()
def upload():
    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"message": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "" or not _allowed_file(file.filename):
        return jsonify({"message": "Please upload a valid PDF file"}), 400

    file_bytes = file.read()
    if not file_bytes:
        return jsonify({"message": "Uploaded file is empty"}), 400

    try:
        extracted_text = extract_text_from_pdf(io.BytesIO(file_bytes))
    except Exception as exc:  # malformed PDF, etc.
        return jsonify({"message": f"Could not read PDF: {exc}"}), 422

    try:
        file_url = upload_resume(io.BytesIO(file_bytes), filename=f"{user_id}_{file.filename}")
    except Exception as exc:
        return jsonify({"message": f"Upload to storage failed: {exc}"}), 502

    resume = Resume(
        user_id=user_id,
        filename=file.filename,
        file_url=file_url,
        extracted_text=extracted_text,
    )
    db.session.add(resume)
    db.session.commit()

    return jsonify(resume.to_dict()), 201


@resume_bp.get("/")
@jwt_required()
def list_resumes():
    user_id = get_jwt_identity()
    resumes = (
        Resume.query.filter_by(user_id=user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    return jsonify([r.to_dict() for r in resumes]), 200


@resume_bp.delete("/<int:resume_id>")
@jwt_required()
def delete_resume(resume_id):
    user_id = get_jwt_identity()
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    if not resume:
        return jsonify({"message": "Resume not found"}), 404

    db.session.delete(resume)
    db.session.commit()
    return jsonify({"message": "Resume deleted"}), 200
