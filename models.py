from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from backend.database import Base
import datetime

class Venue(Base):
    __tablename__ = "venues"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    meta = Column(Text, nullable=True)

class Node(Base):
    __tablename__ = "nodes"
    id = Column(String, primary_key=True)
    venue_id = Column(String, ForeignKey("venues.id"))
    label = Column(String)
    x = Column(Float, nullable=True)
    y = Column(Float, nullable=True)

class Edge(Base):
    __tablename__ = "edges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    venue_id = Column(String, ForeignKey("venues.id"))
    from_node = Column(String)
    to_node = Column(String)
    distance_m = Column(Float, default=1.0)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    venue_id = Column(String, ForeignKey("venues.id"))
    title = Column(String)
    hall_id = Column(String)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text, nullable=True)
