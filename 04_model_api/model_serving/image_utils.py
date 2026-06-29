from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from PIL import Image

from .config import ALLOWED_CONTENT_TYPES, ALLOWED_IMAGE_EXTENSIONS, ANNOTATED_DIR, UPLOAD_DIR


def ensure_output_dirs() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)


def validate_upload(file: UploadFile) -> str:
    original_name = Path(file.filename or "uploaded_image").name
    suffix = Path(original_name).suffix.lower()

    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise HTTPException(status_code=400, detail=f"Unsupported image extension. Use: {allowed}")

    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        allowed = ", ".join(sorted(ALLOWED_CONTENT_TYPES))
        raise HTTPException(status_code=400, detail=f"Unsupported content type. Use: {allowed}")

    return original_name


def save_upload(file_bytes: bytes, original_name: str) -> Path:
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    ensure_output_dirs()
    suffix = Path(original_name).suffix.lower()
    upload_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    upload_path.write_bytes(file_bytes)

    try:
        with Image.open(upload_path) as image:
            image.verify()
    except Exception as exc:
        upload_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.") from exc

    return upload_path


def image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        return image.size


def annotated_output_path(input_path: Path) -> Path:
    ensure_output_dirs()
    return ANNOTATED_DIR / f"{input_path.stem}_annotated.jpg"
