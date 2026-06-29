# Model API

FastAPI REST service for running YOLO inference on Gram-stained bacteria
microscope images.

The API can be run locally for development or through Docker for a more
reproducible deployment-style environment.

## Features

- `GET /`: API overview
- `GET /health`: service health and available model check
- `GET /models`: configured model checkpoints and load status
- `POST /predict`: upload an image and receive object detection results
- `GET /docs`: Swagger UI for testing the API in a browser

## Project Structure

```text
04_model_api/
  server.py
  requirements.txt
  Dockerfile
  .dockerignore
  docker-compose.yml
  README.md

  models/
    clinical/
      best.pt
      last.pt
    pure/
      best.pt
      last.pt

  model_serving/
    config.py
    image_utils.py
    model.py
    schemas.py
```

## Model Artifacts

The API uses the saved checkpoints from Part 3:

```text
04_model_api/models/pure/best.pt
04_model_api/models/clinical/best.pt
```

Available model keys:

```text
pure
clinical
```

## Run Locally

Run these commands from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r 04_model_api\requirements.txt
uvicorn 04_model_api.server:app --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Run with Docker

Run this command from the project root:

```powershell
docker compose -f 04_model_api/docker-compose.yml up --build
```

The API will be available at:

```text
http://localhost:8000
http://localhost:8000/docs
```

Stop the service:

```powershell
docker compose -f 04_model_api/docker-compose.yml down
```

## Example Prediction

PowerShell:

```powershell
curl.exe -X POST "http://localhost:8000/predict" `
  -F "file=@assets/clinical_poscoc.jpg" `
  -F "model=clinical" `
  -F "conf=0.25" `
  -F "save_annotated=true"
```

Response shape:

```json
{
  "model": "clinical",
  "filename": "clinical_poscoc.jpg",
  "image_width": 640,
  "image_height": 640,
  "object_count": 3,
  "detections": [
    {
      "class_id": 1,
      "class_name": "Gram-positive cocci",
      "confidence": 0.87,
      "box": {
        "x1": 100.0,
        "y1": 80.0,
        "x2": 160.0,
        "y2": 130.0
      }
    }
  ],
  "annotated_image_path": "04_model_api/outputs/annotated/example_annotated.jpg",
  "annotated_image_url": "/outputs/annotated/example_annotated.jpg",
  "inference_time_ms": 120.5
}
```

Annotated images are saved under:

```text
04_model_api/outputs/annotated
```
