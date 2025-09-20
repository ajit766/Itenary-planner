## Itinerary Planner — Developer Setup and Run Guide

This repo contains a conversation-first itinerary planning prototype. The AI agents (powered by Google AI Developer Kit - ADK) collect trip basics, educate on destinations, and coordinate a sequential workflow.

### 1) Prerequisites
- Python 3.13 (recommended to match the repo's `venv`)
- git 
- A Google Gemini API key or access to Vertex AI
  - Option A: Gemini API key (`GOOGLE_API_KEY`)
  - Option B: Vertex AI with Application Default Credentials (`gcloud auth application-default login`)

### 2) Clone and set up virtual environment
```bash
git clone <repo-url>
cd Itenary-planner

# Create venv with your local Python 3.13
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

The project currently depends on:
```text
google-adk
```

### 3) Configure model access

Pick one of the following options.

- Option A — Gemini API (hosted API):
```bash
export GOOGLE_API_KEY="<your_gemini_api_key>"
```

- Option B — Vertex AI (GCP project):
```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="<your_gcp_project_id>"
# Optional but recommended defaults
export GOOGLE_CLOUD_REGION="us-central1"
```

Notes:
- If you use a service account, set `GOOGLE_APPLICATION_CREDENTIALS` to the JSON key path instead of using ADC.
- Make sure the selected model (e.g., `gemini-2.5-pro`) is available for your chosen access method.

### 4) Repository layout
- `itenary-agents/agent.py`: Defines the agents including the trip basics collector and the coordinator (`root_agent`).
- `ARCHITECTURE.md`, `REQUIREMENTS.md`, `SEQUENTIAL_WORKFLOW_DESIGN.md`: Background docs on scope and system design.
- `requirements.txt`: Python dependencies.

### 5) Quick smoke test (loads agents)
This verifies that the agent definitions load without import errors.

```bash
source venv/bin/activate
python - <<'PY'
import runpy
ns = runpy.run_path("itenary-agents/agent.py")
agent = ns.get("root_agent")
print("Loaded root agent:", getattr(agent, "name", type(agent)))
PY
```

If this prints a name like `trip_planner_coordinator`, the definitions loaded correctly and your credentials can be configured next to enable real model calls.

### 6) Running the sequential workflow (notes)
The repo currently exposes agent definitions but does not yet include a CLI or server entrypoint. You have a few options to experiment:

- Interactive Python exploration:
  - Use the runpy snippet above to obtain `root_agent`.
  - Depending on the ADK version, the agent object typically supports higher-level orchestration methods. Consult the ADK docs for the exact invocation pattern for `LlmAgent` (e.g., session creation, `respond`/`run`/`start`-style APIs).

- Build a minimal CLI wrapper (future work):
  - Create a small `scripts/run_workflow.py` that imports `root_agent` and starts a conversation loop.

- Server integration (future work):
  - Wire these agents into a FastAPI/uvicorn service and expose endpoints for the UI.

### 7) Common issues
- Module import errors for the `itenary-agents` folder:
  - The folder name contains a hyphen, so import via standard `import itenary-agents` will fail. Use `runpy.run_path("itenary-agents/agent.py")` as shown above, or rename the folder to a valid Python package name (e.g., `itenary_agents`) if you plan to import it.

- Authentication failures:
  - Ensure either `GOOGLE_API_KEY` is set (Gemini API) or ADC is configured for Vertex AI with a project that has access to the chosen model.

### 8) Next steps (recommended)
- Add a CLI entrypoint to start the sequential workflow locally.
- Implement a small FastAPI app to expose a chat endpoint using these agents.
- Parameterize model, temperature, and safety settings via environment variables.

### 9) License and contributions
Internal project. Contributions should be made via PRs on feature branches.


