# app/clients.py
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from .helpers import get_json

load_dotenv()

TOPICS_API_BASE = os.getenv("TOPICS_API_BASE", "http://localhost:5000").rstrip("/")
RESOURCES_API_BASE = os.getenv("RESOURCES_API_BASE", "http://localhost:5002").rstrip("/")

def fetch_topics() -> List[Dict[str, Any]]:
    return get_json(f"{TOPICS_API_BASE}/topics")

def fetch_skills() -> List[Dict[str, Any]]:
    return get_json(f"{TOPICS_API_BASE}/skills")

def fetch_resources() -> List[Dict[str, Any]]:
    items = get_json(f"{RESOURCES_API_BASE}/resources")
    for it in items:
        if "id" not in it and "_id" in it:
            it["id"] = str(it["_id"])
    return items