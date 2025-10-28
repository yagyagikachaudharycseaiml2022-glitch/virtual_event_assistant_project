import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from backend.navigation import build_graph, dijkstra
from backend.nlp import parse_origin_destination
from backend.database import SessionLocal, engine, Base
import backend.crud, backend.qr_gen
from sqlalchemy.orm import Session
from pathlib import Path

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Virtual Event Assistant (Python)")

DATA_DIR = Path("data/venues")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NavRequest(BaseModel):
    venue_id: str
    origin: str = None
    destination: str = None
    text: str = None

@app.post("/venues/upload")
async def upload_venue(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    blueprint = json.loads(content.decode('utf-8'))
    if 'venue_id' not in blueprint:
        raise HTTPException(400, "blueprint missing venue_id")
    out_path = DATA_DIR / f"{blueprint['venue_id']}.json"
    out_path.write_text(json.dumps(blueprint, indent=2))
    crud.create_venue_from_blueprint(db, blueprint)
    url = f"https://example.com/venue/{blueprint['venue_id']}"
    qr_path = qr_gen.make_qr(url, out_file=str(DATA_DIR / f"{blueprint['venue_id']}_qr.png"))
    return {"venue_id": blueprint['venue_id'], "saved": str(out_path), "qr": qr_path}

@app.post("/navigate")
def navigate(req: NavRequest, db: Session = Depends(get_db)):
    origin = req.origin
    destination = req.destination
    if req.text:
        o,d = parse_origin_destination(req.text)
        origin = origin or o
        destination = destination or d
    if not origin or not destination:
        raise HTTPException(400, "origin and destination required (or provide 'text' for NLP parsing)")
    blueprint = crud.get_blueprint_from_db(db, req.venue_id)
    if not blueprint['nodes']:
        file_path = DATA_DIR / f"{req.venue_id}.json"
        if not file_path.exists():
            raise HTTPException(404, "venue blueprint not found")
        blueprint = json.loads(file_path.read_text())
    graph = build_graph(blueprint['nodes'], blueprint['edges'])
    res = dijkstra(graph, origin, destination)
    if not res:
        raise HTTPException(404, "no path found")
    id_to_node = {n['id']: n for n in blueprint['nodes']}
    path_with_labels = [ {"id": nid, "label": id_to_node.get(nid,{}).get('label', nid),
                          "x": id_to_node.get(nid,{}).get('x'), "y": id_to_node.get(nid,{}).get('y')}
                        for nid in res['path'] ]
    return {"distance_m": res['distance_m'], "path": path_with_labels}

@app.get("/venue/{venue_id}/qr")
def get_qr(venue_id: str):
    qr_file = Path(f"data/venues/{venue_id}_qr.png")
    if not qr_file.exists():
        raise HTTPException(404, "QR not found")
    return {"qr_path": str(qr_file)}
