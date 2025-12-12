Project: Virtual Event Assistant (Demo)
--------------------------------------
This package contains a minimal end-to-end demo:
  - backend: FastAPI (Python)
  - frontend: HTML/JS that uses browser STT/TTS and calls backend /navigate
  - sample venue blueprint for Pragati Maidan
To run:
  1. cd backend
  2. python -m venv .venv
  3. source .venv/bin/activate
  4. pip install -r requirements.txt
  5. uvicorn app:app --reload --host 0.0.0.0 --port 8000
Notes:
  - For demo, frontend fetches blueprint from /data/venues path; in production, serve static files or adjust endpoints.
  - No harmful content included.
