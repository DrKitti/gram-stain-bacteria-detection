from __future__ import annotations

import os
from pathlib import Path


API_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_ROOT = Path(os.getenv("MODEL_API_OUTPUT_DIR", API_ROOT / "outputs")).resolve()
UPLOAD_DIR = OUTPUT_ROOT / "uploads"
ANNOTATED_DIR = OUTPUT_ROOT / "annotated"

CLASS_NAMES = {
    0: "Gram-negative cocci",
    1: "Gram-positive cocci",
    2: "Gram-negative bacilli",
    3: "Gram-positive bacilli",
}

MODEL_CONFIGS = {
    "pure": {
        "display_name": "Pure Culture YOLO11m",
        "weights": API_ROOT / "models" / "pure" / "best.pt",
    },
    "clinical": {
        "display_name": "Clinical Specimen YOLO11m",
        "weights": API_ROOT / "models" / "clinical" / "best.pt",
    },
}

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
