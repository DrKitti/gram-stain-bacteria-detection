from __future__ import annotations

from pydantic import BaseModel, Field


class ApiInfo(BaseModel):
    name: str
    version: str
    docs_url: str
    endpoints: list[str]


class HealthResponse(BaseModel):
    status: str
    available_models: list[str]
    output_dir: str


class ModelInfo(BaseModel):
    key: str
    display_name: str
    weights_path: str
    weights_found: bool
    loaded: bool


class BoundingBox(BaseModel):
    x1: float = Field(..., description="Left pixel coordinate")
    y1: float = Field(..., description="Top pixel coordinate")
    x2: float = Field(..., description="Right pixel coordinate")
    y2: float = Field(..., description="Bottom pixel coordinate")


class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    box: BoundingBox


class PredictionResponse(BaseModel):
    model: str
    filename: str
    image_width: int
    image_height: int
    object_count: int
    detections: list[Detection]
    annotated_image_path: str | None = None
    annotated_image_url: str | None = None
    inference_time_ms: float
