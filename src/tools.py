import os
from pymongo import MongoClient

# ── MongoDB Connection ─────────────────────────────────────────────────────
# host.docker.internal = your laptop from inside Docker container
MONGO_HOST = os.getenv("MONGO_HOST", "host.docker.internal")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_URI  = f"mongodb://admin:admin123@{MONGO_HOST}:{MONGO_PORT}/fifa2026?authSource=admin"

def get_client():
    client = MongoClient(MONGO_URI)
    return client["fifa2026"]


# ── Tool 1: Get all venues ─────────────────────────────────────────────────
def get_all_venues() -> list[dict]:
    """
    Returns all FIFA 2026 host venues (stadiums).
    Use this when the user asks about stadiums, venues, or host cities.
    """
    db = get_client()
    venues = list(db.venues.find({}, {"_id": 0})) 
    # first  {} = no filter = give me ALL documents,
    # second {} = hide the _id field (we don't need it) 
    # list convert MongoDB cursor to a plain Python list 
    return venues


# ── Tool 2: Get all teams ──────────────────────────────────────────────────
def get_all_teams() -> list[dict]:
    """
    Returns all teams participating in FIFA 2026.
    Use this when the user asks about countries, nations, or teams.
    """
    db = get_client()
    teams = list(db.teams.find({}, {"_id": 0}))
    return teams


# ── Tool 3: Get all matches ────────────────────────────────────────────────
def get_all_matches() -> list[dict]:
    """
    Returns all FIFA 2026 matches (group stage + final).
    Use this when the user asks about fixtures, games, or schedule.
    """
    db = get_client()
    matches = list(db.matches.find({}, {"_id": 0}))
    return matches