Virtual Event Assistant - Backend
--------------------------------
This folder contains a minimal FastAPI backend for a Virtual Event Assistant.
It supports:
  - uploading venue blueprints (JSON)
  - computing indoor routes (/navigate)
  - generating QR images for venue URLs

Run:
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app:app --reload --host 0.0.0.0 --port 8000
