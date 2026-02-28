import requests
import zipfile
import io
import os
from tqdm import tqdm

from .utils import normalize_segment, ensure_dir

def download_zip(url: str) -> bytes:
    print(f"Downloading: {url}")
    res = requests.get(url)
    res.raise_for_status()
    return res.content

def extract_and_save_step(zip_bytes: bytes, save_dir: str, part_name: str):
    """
    Extract STEP file from zip bytes; save into save_dir with part_name.step
    """
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    step_files = [f for f in z.namelist() if f.lower().endswith(".step")]

    if not step_files:
        print(f"No STEP file found in zip for {part_name}")
        return

    # If multiple, pick the first
    step_filename = step_files[0]
    data = z.read(step_filename)

    ensure_dir(save_dir)

    out_path = os.path.join(save_dir, f"{part_name}.step")

    if os.path.exists(out_path):
        print(f"SKIP (exists): {out_path}")
        return

    with open(out_path, "wb") as f:
        f.write(data)

    print(f"Saved: {out_path}")