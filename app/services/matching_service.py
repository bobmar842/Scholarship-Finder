import re

import numpy as np
import requests
from flask import current_app

# A small, extensible list of common technical/soft skills to look for.
# Extend this list (or load it from a file/DB) as needed.
COMMON_SKILLS = [
    "python", "java", "javascript", "typescript", "react", "node.js", "express",
    "flask", "django", "sql", "mongodb", "postgresql", "mysql", "aws", "azure",
    "gcp", "docker", "kubernetes", "git", "machine learning", "deep learning",
    "nlp", "data analysis", "data science", "pandas", "numpy", "tensorflow",
    "pytorch", "rest api", "graphql", "html", "css", "c++", "c#", "go", "rust",
    "linux", "ci/cd", "agile", "scrum", "communication", "leadership",
    "project management", "problem solving", "testing", "unit testing",
]


def _get_embedding(text: str) -> np.ndarray:
    """Fetch a sentence embedding from the Hugging Face Inference API."""
    token = current_app.config.get("HUGGINGFACE_TOKEN")
    model = current_app.config.get("HF_EMBEDDING_MODEL")

    if not token:
        raise RuntimeError("HUGGINGFACE_TOKEN is not configured")

    url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        url,
        headers=headers,
        json={"inputs": text, "options": {"wait_for_model": True}},
        timeout=30,
    )
    response.raise_for_status()

    arr = np.array(response.json(), dtype=float)
    # Some models return token-level embeddings (2D); mean-pool to a single vector.
    if arr.ndim > 1:
        arr = arr.mean(axis=0)
    return arr


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a, b = a.flatten(), b.flatten()
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def extract_skills(text: str) -> set:
    """Naive keyword-based skill extraction (case-insensitive, whole-word)."""
    text_lower = text.lower()
    found = set()
    for skill in COMMON_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def compute_match(resume_text: str, job_description: str) -> dict:
    """
    Score how well a resume matches a job description.

    Combines semantic similarity (via HF sentence embeddings) with a
    keyword-overlap check against a known skills list, and returns which
    job-relevant skills are present vs. missing from the resume.
    """
    resume_embedding = _get_embedding(resume_text)
    job_embedding = _get_embedding(job_description)
    similarity = _cosine_similarity(resume_embedding, job_embedding)
    match_score = max(0.0, min(1.0, similarity)) * 100

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    return {
        "match_score": match_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
