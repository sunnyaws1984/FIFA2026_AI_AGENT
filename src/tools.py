"""
tools.py
--------
MongoDB query tools exposed to the Google ADK agent.
Each function = one tool the agent can call.
"""

from pymongo import MongoClient

# ── MongoDB Connection ─────────────────────────────────────────────────────
MONGO_URI = "mongodb://admin:admin123@localhost:27017/fifa2026?authSource=admin"

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


# ── Tool 4: Get teams by group ─────────────────────────────────────────────
def get_teams_by_group(group: str) -> list[dict]:
    """
    Returns all teams in a specific group (e.g. "A", "B", "C", "D").
    Use this when the user asks about a specific group.

    Args:
        group: The group letter, e.g. "A"
    """
    db = get_client()
    teams = list(db.teams.find({"group": group.upper()}, {"_id": 0}))
    return teams


# ── Tool 5: Get matches by team ────────────────────────────────────────────
def get_matches_by_team(team_name: str) -> list[dict]:
    """
    Returns all matches involving a specific team.
    Use this when user asks about a specific country's matches.

    Args:
        team_name: The team name, e.g. "Brazil"
    """
    db = get_client()
    matches = list(db.matches.find(
        {"$or": [
            {"home_team": {"$regex": team_name, "$options": "i"}},
            {"away_team": {"$regex": team_name, "$options": "i"}}
        ]},
        {"_id": 0}
    ))
    return matches


# ── Tool 6: Get venues by country ─────────────────────────────────────────
def get_venues_by_country(country: str) -> list[dict]:
    """
    Returns all venues in a specific host country (USA, Mexico, Canada).
    Use this when the user asks about venues in a particular country.

    Args:
        country: Country name, e.g. "USA"
    """
    db = get_client()
    venues = list(db.venues.find(
        {"country": {"$regex": country, "$options": "i"}},
        {"_id": 0}
    ))
    return venues


# ── Tool 7: Get match by stage ─────────────────────────────────────────────
def get_matches_by_stage(stage: str) -> list[dict]:
    """
    Returns matches filtered by stage: "Group Stage" or "Final".
    Use this when user asks about group stage matches or the final.

    Args:
        stage: e.g. "Group Stage" or "Final"
    """
    db = get_client()
    matches = list(db.matches.find(
        {"stage": {"$regex": stage, "$options": "i"}},
        {"_id": 0}
    ))
    return matches
