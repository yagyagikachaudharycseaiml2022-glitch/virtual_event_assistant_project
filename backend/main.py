"""main.py - single-step runner for the Virtual Event Assistant project.

Usage (after creating and activating a virtualenv and installing requirements):
    python main.py
or (alternative)
    uvicorn main:app --reload

This file re-uses the FastAPI app created in backend/app.py and mounts the frontend/
directory as StaticFiles at the root path, so opening http://localhost:8000 serves the
frontend and backend endpoints remain available under their paths (e.g., /navigate).
"""

from pathlib import Path
import sys
from fastapi.staticfiles import StaticFiles
import uvicorn

# Try to import the FastAPI app defined in backend/app.py
try:
    # backend.app defines `app = FastAPI(...)`
    from backend.app import app as backend_app  # type: ignore
except Exception as e:
    raise RuntimeError("Failed to import backend.app. Make sure you're running from the project root and dependencies are installed. Import error: {}".format(e))

app = backend_app

# Mount the frontend static files at root (if present)
frontend_dir = Path(__file__).parent / "frontend"
if frontend_dir.exists() and frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    print("Warning: frontend directory not found. The backend will still run but no static UI will be served.")


if __name__ == '__main__':
    # Run uvicorn programmatically
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Open in browser automatically
    import webbrowser
    webbrowser.open("http://127.0.0.1:8000/")