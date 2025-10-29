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
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, Base
import crud, qr_gen
from navigation import build_graph, dijkstra
from nlp import parse_origin_destination

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Virtual Event Assistant Backend")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "Backend is running successfully on Render 🚀"}

# ✅ Route: Generate QR code
@app.post("/generate-qr/")
async def generate_qr(data: dict):
    try:
        qr_path = qr_gen.generate_qr(data)
        return {"qr_code_path": qr_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Route: Shortest path
@app.post("/shortest-path/")
async def find_shortest_path(request: dict):
    try:
        graph = build_graph()
        origin = request.get("origin")
        destination = request.get("destination")
        distance, path = dijkstra(graph, origin, destination)
        return {"distance": distance, "path": path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Route: NLP Parse
@app.post("/parse/")
async def parse_query(query: dict):
    try:
        text = query.get("text")
        origin, destination = parse_origin_destination(text)
        return {"origin": origin, "destination": destination}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Mount frontend (if exists)
frontend_dir = Path(__file__).parent / "../frontend/build"
if frontend_dir.exists() and frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    print("⚠️  Frontend directory not found — backend will run without UI")

# ✅ For local run
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
