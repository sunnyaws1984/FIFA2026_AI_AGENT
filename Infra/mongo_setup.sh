#!/bin/bash
# ─────────────────────────────────────────────────────
#  FIFA 2026 — Seed Data Script
#  Populates: venues + matches collections (Dummy data for demo)
# ─────────────────────────────────────────────────────

NAMESPACE="fifa2026"
MONGO_USER="admin"
MONGO_PASS="admin123"
POD=$(kubectl get pod -n $NAMESPACE -l app=mongodb -o jsonpath='{.items[0].metadata.name}')

echo "🌱 Seeding FIFA 2026 data into pod: $POD"

kubectl exec -n $NAMESPACE $POD -- mongosh \
  -u $MONGO_USER -p $MONGO_PASS \
  --authenticationDatabase admin \
  --eval '

// ── Switch to fifa2026 database ──────────────────────
use("fifa2026");

// ── Drop existing collections (clean slate) ──────────
db.venues.drop();
db.matches.drop();
db.teams.drop();

// ════════════════════════════════════════════════════
// 1. VENUES — Host stadiums
// ════════════════════════════════════════════════════
db.venues.insertMany([
  {
    venue_id: "V01",
    name: "MetLife Stadium",
    city: "New York",
    country: "USA",
    capacity: 82500
  },
  {
    venue_id: "V02",
    name: "AT&T Stadium",
    city: "Dallas",
    country: "USA",
    capacity: 80000
  },
  {
    venue_id: "V03",
    name: "SoFi Stadium",
    city: "Los Angeles",
    country: "USA",
    capacity: 70240
  },
  {
    venue_id: "V04",
    name: "Estadio Azteca",
    city: "Mexico City",
    country: "Mexico",
    capacity: 87523
  },
  {
    venue_id: "V05",
    name: "BC Place",
    city: "Vancouver",
    country: "Canada",
    capacity: 54500
  }
]);
print("✅ Venues inserted: " + db.venues.countDocuments());

// ════════════════════════════════════════════════════
// 2. TEAMS — Participating nations
// ════════════════════════════════════════════════════
db.teams.insertMany([
  { team_id: "T01", name: "Brazil",    group: "A", confederation: "CONMEBOL" },
  { team_id: "T02", name: "Germany",   group: "A", confederation: "UEFA"     },
  { team_id: "T03", name: "Argentina", group: "B", confederation: "CONMEBOL" },
  { team_id: "T04", name: "France",    group: "B", confederation: "UEFA"     },
  { team_id: "T05", name: "England",   group: "C", confederation: "UEFA"     },
  { team_id: "T06", name: "Spain",     group: "C", confederation: "UEFA"     },
  { team_id: "T07", name: "USA",       group: "D", confederation: "CONCACAF" },
  { team_id: "T08", name: "Mexico",    group: "D", confederation: "CONCACAF" }
]);
print("✅ Teams inserted: " + db.teams.countDocuments());

// ════════════════════════════════════════════════════
// 3. MATCHES — Group stage fixtures
// ════════════════════════════════════════════════════
db.matches.insertMany([
  {
    match_id: "M01",
    stage: "Group Stage",
    group: "A",
    home_team: "Brazil",
    away_team: "Germany",
    venue: "MetLife Stadium",
    city: "New York",
    date: "2026-06-11",
    time: "18:00",
    status: "scheduled",
    score: null
  },
  {
    match_id: "M02",
    stage: "Group Stage",
    group: "B",
    home_team: "Argentina",
    away_team: "France",
    venue: "AT&T Stadium",
    city: "Dallas",
    date: "2026-06-12",
    time: "20:00",
    status: "scheduled",
    score: null
  },
  {
    match_id: "M03",
    stage: "Group Stage",
    group: "C",
    home_team: "England",
    away_team: "Spain",
    venue: "SoFi Stadium",
    city: "Los Angeles",
    date: "2026-06-13",
    time: "15:00",
    status: "scheduled",
    score: null
  },
  {
    match_id: "M04",
    stage: "Group Stage",
    group: "D",
    home_team: "USA",
    away_team: "Mexico",
    venue: "Estadio Azteca",
    city: "Mexico City",
    date: "2026-06-14",
    time: "21:00",
    status: "scheduled",
    score: null
  },
  {
    match_id: "M05",
    stage: "Final",
    group: null,
    home_team: "TBD",
    away_team: "TBD",
    venue: "MetLife Stadium",
    city: "New York",
    date: "2026-07-19",
    time: "18:00",
    status: "scheduled",
    score: null
  }
]);
print("✅ Matches inserted: " + db.matches.countDocuments());

// ════════════════════════════════════════════════════
// 4. VERIFY — Quick summary
// ════════════════════════════════════════════════════
print("");
print("─────────────────────────────────");
print("📊 FIFA 2026 Database Summary");
print("─────────────────────────────────");
print("Venues  : " + db.venues.countDocuments());
print("Teams   : " + db.teams.countDocuments());
print("Matches : " + db.matches.countDocuments());
print("─────────────────────────────────");
print("");

// Sample queries students can try:
print("💡 Try these queries in mongosh:");
print("   db.venues.find()");
print("   db.matches.find({ stage: \"Group Stage\" })");
print("   db.matches.find({ home_team: \"USA\" })");
print("   db.teams.find({ group: \"A\" })");
'

echo ""
echo "🎉 Seeding complete!"
echo ""
echo "  Open MongoDB shell:"
echo "    kubectl exec -it -n $NAMESPACE $POD -- mongosh -u $MONGO_USER -p $MONGO_PASS --authenticationDatabase admin"
echo ""
echo "  Then run:"
echo "    use fifa2026"
echo "    db.venues.find().pretty()"
echo "    db.matches.find().pretty()"
echo "    db.teams.find().pretty()"