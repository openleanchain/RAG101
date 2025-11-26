# workshop2/incident_rag/triage_config.py

from pathlib import Path

# Root of workshop2
BASE_DIR = Path(__file__).resolve().parents[1]

# Paths to Workshop 2 data
DATA_DIR = BASE_DIR / "data"
POLICIES_DIR = DATA_DIR / "policies"
INDEX_DIR = DATA_DIR / "index"
PROMPTS_DIR = DATA_DIR / "prompts"
LOGS_DIR = DATA_DIR / "logs"

# Reuse MiniLM embedding model from the kids rag_demo:
# workshop2/rag_demo/data/models/
RAG_DEMO_MODELS_DIR = BASE_DIR / "rag_demo" / "data" / "models"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_MODEL_DIR = RAG_DEMO_MODELS_DIR  # reuse same folder

# LLM configuration (adjust to your environment)
# For Azure OpenAI, this is typically your deployment name
TRIAGE_LLM_MODEL = "gpt-4.1-mini"  # placeholder; replace with your deployment name

# Ensure core directories exist
for d in [POLICIES_DIR, INDEX_DIR, PROMPTS_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
