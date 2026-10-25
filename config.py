import os


def _load_key():
    key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    key_file = os.path.join(os.path.dirname(__file__), "key.txt")
    if os.path.exists(key_file):
        with open(key_file, "r", encoding="utf-8") as f:
            key = f.read().strip()
    if key:
        return key
    project1_key = os.path.join(
        os.path.dirname(__file__), "..", "code-review-agent", "key.txt"
    )
    if os.path.exists(project1_key):
        with open(project1_key, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


DEEPSEEK_API_KEY = _load_key()
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

MAX_REVIEW_ROUNDS = 3
TEMPERATURE = 0.3
