from dotenv import load_dotenv
from pathlib import Path

# Load .env from root explicitly
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")
