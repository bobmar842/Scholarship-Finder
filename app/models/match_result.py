from datetime import datetime

from app.extensions import db


class MatchResult(db.Model):
    __tablename__ = "match_results"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Float, nullable=False)  # 0-100
    matched_keywords = db.Column(db.Text, nullable=True)  # comma-separated
    missing_keywords = db.Column(db.Text, nullable=True)  # comma-separated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "match_score": round(self.match_score, 2),
            "matched_keywords": self.matched_keywords.split(",") if self.matched_keywords else [],
            "missing_keywords": self.missing_keywords.split(",") if self.missing_keywords else [],
            "created_at": self.created_at.isoformat(),
        }
