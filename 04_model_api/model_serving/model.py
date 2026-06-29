from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from PIL import Image

from .config import CLASS_NAMES, MODEL_CONFIGS
from .image_utils import annotated_output_path, image_size
from .schemas import BoundingBox, Detection, ModelInfo, PredictionResponse


class YoloModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, Any] = {}

    def model_infos(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                key=model_key,
                display_name=str(config["display_name"]),
                weights_path=str(Path(config["weights"]).resolve()),
                weights_found=Path(config["weights"]).exists(),
                loaded=model_key in self._models,
            )
            for model_key, config in MODEL_CONFIGS.items()
        ]

    def available_model_keys(self) -> list[str]:
        return list(MODEL_CONFIGS.keys())

    def load(self, model_key: str) -> Any:
        if model_key not in MODEL_CONFIGS:
            available = ", ".join(self.available_model_keys())
            raise HTTPException(status_code=400, detail=f"Unknown model '{model_key}'. Use: {available}")

        if model_key not in self._models:
            weights_path = Path(MODEL_CONFIGS[model_key]["weights"]).resolve()
            if not weights_path.exists():
                raise HTTPException(status_code=503, detail=f"Model weights not found: {weights_path}")

            from ultralytics import YOLO

            self._models[model_key] = YOLO(str(weights_path))

        return self._models[model_key]

    def predict(
        self,
        *,
        model_key: str,
        image_path: Path,
        original_filename: str,
        conf: float,
        iou: float,
        max_det: int,
        save_annotated: bool,
    ) -> PredictionResponse:
        model = self.load(model_key)
        width, height = image_size(image_path)

        start = time.perf_counter()
        results = model.predict(
            source=str(image_path),
            conf=conf,
            iou=iou,
            max_det=max_det,
            verbose=False,
        )
        inference_time_ms = (time.perf_counter() - start) * 1000

        result = results[0]
        detections = self._extract_detections(result)

        annotated_path = None
        annotated_url = None
        if save_annotated:
            annotated_path = annotated_output_path(image_path)
            plotted = result.plot()
            Image.fromarray(plotted[..., ::-1]).save(annotated_path)
            annotated_url = f"/outputs/annotated/{annotated_path.name}"

        return PredictionResponse(
            model=model_key,
            filename=original_filename,
            image_width=width,
            image_height=height,
            object_count=len(detections),
            detections=detections,
            annotated_image_path=str(annotated_path) if annotated_path else None,
            annotated_image_url=annotated_url,
            inference_time_ms=round(inference_time_ms, 2),
        )

    def _extract_detections(self, result: Any) -> list[Detection]:
        detections: list[Detection] = []
        boxes = result.boxes

        if boxes is None:
            return detections

        xyxy = boxes.xyxy.cpu().tolist()
        classes = boxes.cls.cpu().tolist()
        confidences = boxes.conf.cpu().tolist()

        for box_values, class_value, confidence in zip(xyxy, classes, confidences):
            class_id = int(class_value)
            detections.append(
                Detection(
                    class_id=class_id,
                    class_name=CLASS_NAMES.get(class_id, str(class_id)),
                    confidence=round(float(confidence), 6),
                    box=BoundingBox(
                        x1=round(float(box_values[0]), 3),
                        y1=round(float(box_values[1]), 3),
                        x2=round(float(box_values[2]), 3),
                        y2=round(float(box_values[3]), 3),
                    ),
                )
            )

        return detections


model_registry = YoloModelRegistry()
