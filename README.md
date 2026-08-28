# CV Align

Resume-to-job-description matcher. Upload a resume (PDF), paste a job
description, and get a semantic match score plus a list of skills the
resume is missing for that role.

## Stack

- **Backend**: Flask (Python), Flask-SQLAlchemy, Flask-JWT-Extended
- **Auth**: JWT (bcrypt-hashed passwords)
- **Storage**: Cloudinary (resume PDFs)
- **Matching**: Hugging Face Inference API (sentence embeddings + cosine
  similarity) combined with keyword/skill overlap detection
- **Database**: SQLite by default (swap `DATABASE_URL` for Postgres/MySQL
  in production)

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp app/.env.example .env        # then fill in your real keys
python run.py                   # runs on http://localhost:5000
```

You'll need:
- A free [Cloudinary](https://cloudinary.com) account (cloud name, API key/secret)
- A free [Hugging Face](https://huggingface.co/settings/tokens) access token

**Never commit your real `.env` file** — only `app/.env.example` (with
placeholders) should be in version control.

## API

| Method | Endpoint                        | Auth | Description                          |
|--------|----------------------------------|------|---------------------------------------|
| GET    | `/api/health`                   | No   | Health check                          |
| POST   | `/api/auth/register`            | No   | Create account, returns JWT           |
| POST   | `/api/auth/login`               | No   | Log in, returns JWT                   |
| POST   | `/api/resume/upload`            | Yes  | Upload a PDF resume (`multipart/form-data`, field `file`) |
| GET    | `/api/resume/`                  | Yes  | List your uploaded resumes            |
| DELETE | `/api/resume/<id>`              | Yes  | Delete a resume                       |
| POST   | `/api/match/`                   | Yes  | `{resume_id, job_description}` → match score + skills |
| GET    | `/api/match/history/<resume_id>`| Yes  | Past match results for a resume       |

Send the JWT as `Authorization: Bearer <token>` on protected routes.

## Project structure

```
app/
  __init__.py          # app factory
  config.py             # env-driven config
  extensions.py         # db, jwt, bcrypt, cors instances
  models/                # User, Resume, MatchResult
  routes/                 # auth, resume, match blueprints
  services/                # pdf extraction, cloudinary upload, HF matching
run.py                      # entry point
requirements.txt
```
