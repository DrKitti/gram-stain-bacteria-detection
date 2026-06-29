from __future__ import annotations

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles

from .model_serving.config import OUTPUT_ROOT
from .model_serving.image_utils import ensure_output_dirs, save_upload, validate_upload
from .model_serving.model import model_registry
from .model_serving.schemas import ApiInfo, HealthResponse, ModelInfo, PredictionResponse


app = FastAPI(
    title="Gram Stain Bacteria Detection API",
    description="YOLO-based object detection API for Gram-stained bacteria microscope images.",
    version="0.1.0",
)

ensure_output_dirs()


@app.on_event("startup")
def startup() -> None:
    ensure_output_dirs()


app.mount("/outputs", StaticFiles(directory=str(OUTPUT_ROOT)), name="outputs")


@app.get("/", response_model=ApiInfo)
def read_root() -> ApiInfo:
    return ApiInfo(
        name="Gram Stain Bacteria Detection API",
        version=app.version,
        docs_url="/docs",
        endpoints=["GET /health", "GET /models", "POST /predict"],
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    available = [info.key for info in model_registry.model_infos() if info.weights_found]
    status = "ok" if available else "missing_models"
    return HealthResponse(
        status=status,
        available_models=available,
        output_dir=str(OUTPUT_ROOT),
    )


@app.get("/models", response_model=list[ModelInfo])
def list_models() -> list[ModelInfo]:
    return model_registry.model_infos()


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(..., description="Input microscope image"),
    model: str = Form("clinical", description="Model key: clinical or pure"),
    conf: float = Form(0.25, ge=0.0, le=1.0, description="Confidence threshold"),
    iou: float = Form(0.7, ge=0.0, le=1.0, description="IoU threshold"),
    max_det: int = Form(1500, ge=1, le=10000, description="Maximum detections"),
    save_annotated: bool = Form(True, description="Save annotated image output"),
) -> PredictionResponse:
    original_name = validate_upload(file)
    file_bytes = await file.read()
    upload_path = save_upload(file_bytes, original_name)

    return model_registry.predict(
        model_key=model,
        image_path=upload_path,
        original_filename=original_name,
        conf=conf,
        iou=iou,
        max_det=max_det,
        save_annotated=save_annotated,
    )
