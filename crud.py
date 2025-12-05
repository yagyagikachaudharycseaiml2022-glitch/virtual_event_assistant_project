from sqlalchemy.orm import Session
from backend.models import Venue, Node, Edge, Event
import json

def create_venue_from_blueprint(db: Session, blueprint: dict):
    vid = blueprint['venue_id']
    venue = Venue(id=vid, name=blueprint.get('name',''), meta=json.dumps(blueprint.get('meta','')))
    db.merge(venue)
    for n in blueprint.get('nodes', []):
        node = Node(id=n['id'], venue_id=vid, label=n.get('label',''), x=n.get('x'), y=n.get('y'))
        db.merge(node)
    for e in blueprint.get('edges', []):
        edge = Edge(venue_id=vid, from_node=e['from'], to_node=e['to'], distance_m=e.get('distance_m', 1.0))
        db.add(edge)
    db.commit()

def get_blueprint_from_db(db: Session, venue_id: str):
    nodes = db.query(Node).filter(Node.venue_id==venue_id).all()
    edges = db.query(Edge).filter(Edge.venue_id==venue_id).all()
    return {
        "venue_id": venue_id,
        "nodes": [ {"id":n.id,"label":n.label,"x":n.x,"y":n.y} for n in nodes ],
        "edges": [ {"from":e.from_node,"to":e.to_node,"distance_m":e.distance_m} for e in edges ]
    }
