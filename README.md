# Gram Stain Bacteria Detection

A senior project for object detection of Gram-stained bacteria in microscope
images. The pipeline detects and classifies bacteria into four clinically
relevant groups:

1. Gram-negative cocci
2. Gram-positive cocci
3. Gram-negative bacilli
4. Gram-positive bacilli

The project uses two data domains:

- `Pure Culture`: cleaner species-based microscope images regrouped into Gram-stain categories
- `Clinical Specimen`: more realistic clinical images used as the main detection dataset

## Project Structure

```text
01_data_analysis.ipynb       # Dataset exploration and visualization
02_benchmark_model.ipynb     # YOLO benchmark result analysis
03_training_model/           # Dataset config, training, evaluation, prediction scripts
04_model_api/                # FastAPI inference service and Docker deployment
benchmark_result/            # Saved benchmark CSV results
assets/                      # Example images used in documentation
data.md                      # Dataset notes and class mapping
requirements.txt             # Full project dependencies
```

## Environment Setup

Install the full project environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks venv activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
```

For API-only usage:

```powershell
python -m pip install -r 04_model_api\requirements.txt
```

## Part 1: Data Analysis

Notebook: `01_data_analysis.ipynb`

This notebook explores dataset size, class distribution, bounding box patterns,
objects per image, and differences between `Pure Culture` and `Clinical Specimen`.

Dataset details and class mapping are documented in [data.md](data.md).

Example images:

| Dataset | Example |
| --- | --- |
| Pure Culture: Gram-positive cocci | ![Pure Culture Gram-positive cocci](assets/pure_culture_poscoc.png) |
| Pure Culture: Gram-negative bacilli | ![Pure Culture Gram-negative bacilli](assets/pure_culture_negbac.png) |
| Clinical Specimen: Gram-positive cocci | ![Clinical Gram-positive cocci](assets/clinical_poscoc.jpg) |
| Clinical Specimen: Gram-negative bacilli | ![Clinical Gram-negative bacilli](assets/clinical_negbac.jpg) |

Run:

```powershell
jupyter notebook 01_data_analysis.ipynb
```

## Part 2: Benchmark Model

Notebook: `02_benchmark_model.ipynb`

This notebook compares saved YOLO training results from `benchmark_result/`.
The selected benchmark rule is the epoch with the highest `mAP@50-95`.

Best benchmark summary:

| Model | Best Epoch | mAP@50 | mAP@50-95 | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| YOLOv11m | 38 | 0.8411 | 0.5172 | 0.7567 | 0.8122 | 0.7835 |
| YOLOv8m | 39 | 0.8355 | 0.5083 | 0.7778 | 0.7785 | 0.7781 |
| YOLOv11s | 50 | 0.8290 | 0.4840 | 0.7387 | 0.8009 | 0.7686 |
| YOLOv8s | 50 | 0.8147 | 0.4746 | 0.7410 | 0.7756 | 0.7579 |
| YOLOv11n | 45 | 0.7527 | 0.4046 | 0.7192 | 0.7313 | 0.7252 |
| YOLOv8n | 50 | 0.7430 | 0.3914 | 0.6992 | 0.7270 | 0.7128 |

Run:

```powershell
jupyter notebook 02_benchmark_model.ipynb
```

## Part 3: Training and Evaluation

Folder: `03_training_model/`

Main scripts:

- `prepare_dataset_configs.py`: create YOLO split files and dataset YAML configs
- `train_final_model.py`: train YOLO11m on `pure`, `clinical`, or `both`
- `evaluate_best_model.py`: evaluate saved `best.pt` checkpoints
- `predict_best_model.py`: run image/folder prediction with saved checkpoints

Expected local dataset folders:

```text
Data/Pure Culture/images
Data/Pure Culture/labels
Data/Clinical Specimen/images
Data/Clinical Specimen/labels
Data/Clinical Specimen/txt
```

Run:

```powershell
python 03_training_model\prepare_dataset_configs.py
python 03_training_model\train_final_model.py --dataset both
python 03_training_model\evaluate_best_model.py --model clinical
python 03_training_model\predict_best_model.py --model clinical --source path\to\images
```

Saved model artifacts are stored under:

```text
04_model_api/models/pure/best.pt
04_model_api/models/clinical/best.pt
```

## Part 4: Model API

Folder: `04_model_api/`

FastAPI service for running YOLO inference through HTTP.

Endpoints:

- `GET /`: API overview
- `GET /health`: service health and available model check
- `GET /models`: model artifact status
- `POST /predict`: upload an image and return detection results
- `GET /docs`: Swagger UI

Run locally:

```powershell
python -m uvicorn 04_model_api.server:app --reload --host 0.0.0.0 --port 8000
```

Run with Docker:

```powershell
docker compose -f 04_model_api/docker-compose.yml up --build
```

Open:

```text
http://localhost:8000/docs
```

Example prediction request:

```powershell
curl.exe -X POST "http://localhost:8000/predict" `
  -F "file=@assets/clinical_poscoc.jpg" `
  -F "model=clinical" `
  -F "conf=0.25" `
  -F "save_annotated=true"
```

Annotated outputs are saved under:

```text
04_model_api/outputs/annotated
```

More API details are in [04_model_api/README.md](04_model_api/README.md).
