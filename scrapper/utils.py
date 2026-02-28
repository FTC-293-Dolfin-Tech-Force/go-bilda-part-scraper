import re
import os

def normalize_segment(name: str) -> str:
    """
    Normalize breadcrumb or part category segment to valid folder name:
    - lowercase
    - spaces -> underscores
    - strip special characters except hyphens
    """
    name = name.lower().strip()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-z0-9_\-]", "", name)
    return name

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)