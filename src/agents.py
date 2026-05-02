"""
agent.py
--------
Google ADK root agent for FIFA 2026 Q&A.
Connects to MongoDB tools and answers questions about
venues, teams, and matches.
"""

from google.adk.agents import Agent

from tools import (
    get_all_venues,
    get_all_teams,
    get_all_matches,
    get_teams_by_group,
    get_matches_by_team,
    get_venues_by_country,
    get_matches_by_stage,
)

# ── Root Agent ─────────────────────────────────────────────────────────────
root_agent = Agent(
    name="fifa2026_agent",

    # Model — use Gemini 1.5 Flash (fast + free tier friendly)
    model="gemini-1.5-flash",

    description="FIFA 2026 Q&A agent that queries a MongoDB database.",

    instruction="""
    You are a helpful FIFA 2026 assistant. You have access to a MongoDB 
    database that contains information about:
      - Venues   : host stadiums across USA, Canada and Mexico
      - Teams    : nations participating in FIFA 2026
      - Matches  : fixtures for group stage and the final

    RULES:
    1. Always use your tools to fetch data — never make up facts.
    2. When asked about stadiums or cities, use get_all_venues or get_venues_by_country.
    3. When asked about teams or countries, use get_all_teams or get_teams_by_group.
    4. When asked about games or fixtures, use get_all_matches, get_matches_by_team,
       or get_matches_by_stage.
    5. Answer in a clear, concise and friendly way.
    6. If the data does not contain the answer, say so honestly.
    """,

    tools=[
        get_all_venues,
        get_all_teams,
        get_all_matches,
        get_teams_by_group,
        get_matches_by_team,
        get_venues_by_country,
        get_matches_by_stage,
    ],
)
