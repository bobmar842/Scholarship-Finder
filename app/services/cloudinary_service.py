from typing import BinaryIO

import cloudinary.uploader


def upload_resume(file_stream: BinaryIO, filename: str) -> str:
    """Upload a resume PDF to Cloudinary and return its secure URL."""
    result = cloudinary.uploader.upload(
        file_stream,
        resource_type="raw",
        public_id=filename,
        folder="cv_align/resumes",
        overwrite=True,
    )
    return result.get("secure_url")
