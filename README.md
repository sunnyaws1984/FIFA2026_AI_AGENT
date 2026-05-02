# FIFA 2026 Agent — Google ADK + MongoDB + Kubernetes

A beginner-friendly AI agent that answers questions about FIFA 2026 venues, teams, and matches.
Built with **Google ADK**, **MongoDB on Kubernetes**, and a **Gradio** chat UI.

---

## Architecture

```
You (Browser)
    │
    ▼
Gradio UI  (ui.py — port 7860)
    │
    ▼
ADK Runner + Root Agent  (agent.py)
    │  Gemini 1.5 Flash decides which tool to call
    ▼
Tools  (tools.py)
    │  Plain Python functions querying MongoDB
    ▼
MongoDB  (Kubernetes — port 27017)
    ├── venues    collection
    ├── teams     collection
    └── matches   collection
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11+ |
| kubectl | any recent |
| Kubernetes | Docker Desktop / minikube / kind |
| Gemini API Key | [Get one free](https://aistudio.google.com/app/apikey) |

---

## Step 1 — Deploy MongoDB on Kubernetes

```bash
# Deploy single-node MongoDB with PersistentVolume
cd Infra
execute both the files you see inside this
```

This creates in the `fifa2026` namespace:
- `Secret` — stores MongoDB credentials
- `PersistentVolume` — 2Gi storage on node disk at `/mnt/fifa2026-mongodb`
- `PersistentVolumeClaim` — claims the PV
- `Deployment` — single MongoDB pod (mongo:7.0)
- `Service` — NodePort exposed on port `32017`

Verify everything is running:
```bash
kubectl get all -n fifa2026
kubectl get pv,pvc -n fifa2026
```

---

## Step 2 — Seed FIFA 2026 Data

```bash
# Populate MongoDB with venues, teams and matches
bash seed-fifa2026.sh
```

This creates 3 collections:

| Collection | Documents | Contains |
|---|---|---|
| `venues` | 5 | Stadiums across USA, Mexico, Canada |
| `teams` | 8 | Participating nations with groups |
| `matches` | 5 | Group stage fixtures + Final |

Verify the data inside MongoDB:
```bash
# Get your pod name
kubectl get pods -n fifa2026

# Open MongoDB shell
kubectl exec -it -n fifa2026 <pod-name> -- mongosh \
  -u admin -p admin123 --authenticationDatabase admin

# Inside mongosh
use fifa2026
show collections
db.venues.find().pretty()
db.teams.find().pretty()
db.matches.find().pretty()
```

---

## Step 3 — Port-Forward MongoDB

Keep this running in a **separate terminal** so your Python app can reach MongoDB:

```bash
kubectl port-forward -n fifa2026 svc/mongodb-service 27017:27017
```

---

## Step 4 — Set Gemini API Key

```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

Get a free key at: https://aistudio.google.com/app/apikey

---

## Step 5 — Install Python Virtual Env and Dependencies

```bash
python -m venv .venv
source .venv/Scripts/Activate
pip install uv
uv pip install -r requirements.txt
```

---

## Step 6 — Run the Agent UI

```bash
python ui.py
```

Open your browser at: **http://localhost:7860**

---

## Example Questions to Ask

```
What venues are hosted in the USA?
Which teams are in Group A?
Tell me about the Final match.
Show me all matches involving Brazil.
How many venues are in Mexico?
List all teams in the tournament.
When does Argentina play?
What is the capacity of MetLife Stadium?
```

---

## How It Works — File by File

### tools.py
Contains 3 plain Python functions. Each function queries one MongoDB collection.
ADK reads the **docstring** of each function to understand when to call it.

```python
def get_all_venues() -> list[dict]:
    """Returns all FIFA 2026 host venues."""
    db = get_client()
    return list(db.venues.find({}, {"_id": 0}))
```

### agent.py
Defines the ADK `root_agent` with:
- **model** — which Gemini model to use
- **instruction** — system prompt telling the agent how to behave
- **tools** — the 3 MongoDB functions it can call

```python
root_agent = Agent(
    name="fifa2026_agent",
    model="gemini-2.5-flash",
    instruction="You are a FIFA 2026 assistant...",
    tools=[get_all_venues, get_all_teams, get_all_matches],
)
```

### ui.py
Gradio chat interface that:
1. Creates an ADK `Runner` with the root agent
2. Creates an in-memory session per user
3. Sends your question to the runner
4. Displays the agent's response in a chat window

---

## MongoDB Connection String

```
mongodb://admin:admin123@localhost:27017/fifa2026?authSource=admin
```

| Field | Value |
|---|---|
| Host | localhost (via port-forward) |
| Port | 27017 |
| Username | admin |
| Password | admin123 |
| Database | fifa2026 |
| Auth DB | admin |

---

## Troubleshooting

**MongoDB pod not running**
```bash
kubectl get pods -n fifa2026
kubectl describe pod <pod-name> -n fifa2026
```

**PVC stuck in Pending**
```bash
kubectl get pvc -n fifa2026
kubectl describe pvc mongodb-pvc -n fifa2026
```

**Agent not responding**
- Make sure port-forward is running in a separate terminal
- Make sure `GOOGLE_API_KEY` is set
- Check MongoDB connection string in `tools.py`

**Reset everything**
```bash
kubectl delete namespace fifa2026
sh -x Infra/k8s_setup.sh
sh -x Infra/mongo_setup.sh
```

---

## Key Concepts Learned

| Concept | Where |
|---|---|
| Kubernetes Namespace | `deploy-mongodb.sh` step 1 |
| Kubernetes Secret | `deploy-mongodb.sh` step 2 |
| PersistentVolume + PVC | `deploy-mongodb.sh` steps 3-4 |
| Kubernetes Deployment | `deploy-mongodb.sh` step 5 |
| Kubernetes Service (NodePort) | `deploy-mongodb.sh` step 6 |
| MongoDB Collections + Documents | `seed-fifa2026.sh` |
| Google ADK Agent + Tools | `agent.py` + `tools.py` |
| ADK Runner + Sessions | `ui.py` |
| Gradio Chat UI | `ui.py` |
