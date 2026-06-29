# Gram Stain Bacteria Detection 🔬🦠

A Senior Project on object detection of Gram-stained bacteria from microscope images.


![Object Detection](https://img.shields.io/badge/Object_Detection-blue?style=flat-square)
![Medical Imaging](https://img.shields.io/badge/Medical_Imaging-green?style=flat-square)
![Computer Vision](https://img.shields.io/badge/Computer_Vision-orange?style=flat-square)
![Deep Learning](https://img.shields.io/badge/Deep_Learning-purple?style=flat-square)


## Project Overview
In this project we studies the detection of bacteria in Gram-stained microscopic images using 4 clinically relevant categories :
1. Gram-negative cocci — Round-shaped bacteria that appear pink or red after laboratory staining
2. Gram-positive cocci — Round-shaped bacteria that appear purple after laboratory staining
3. Gram-negative bacilli — Rod-shaped bacteria that appear pink or red after laboratory staining
4. Gram-positive bacilli — Rod-shaped bacteria that appear purple after laboratory staining

The main goal is to build a detection pipeline that can localize bacteria and classify them into these 4 groups across 2 domains :

- `Pure Culture`, which provides cleaner species-based microscope images that were regrouped into Gram-stain categories
- `Clinical Specimen`, which provides more realistic and visually complex images from clinical samples

And we are organized the project into 4 main parts :

- **Part 1 : Data analysis** for dataset exploration, class distribution study, and Gram-stain bacteria characteristics
- **Part 2 : Benchmark model** for comparing baseline object detection models on the prepared datasets
- **Part 3 : Training model and evaluate** for developing and improving the final bacteria detection pipeline
- **Part 4 : Model API and inference deployment** for running saved models through Docker-based inference

---

## Part 1 : Data Analysis
### Dataset Summary

The repository currently uses two dataset sources:

- `Pure Culture`: regrouped from public species-level bacteria image datasets
- `Clinical Specimen`: annotated clinical detection dataset used as the main real-world source

For more detailed about dataset, source, and full example images you can read in [data.md](data.md).

### Dataset Preview

| Dataset | Example |
| --- | --- |
| Pure Culture: Gram-positive cocci | ![Pure Culture Gram-positive cocci](assets/pure_culture_poscoc.png) |
| Pure Culture: Gram-negative bacilli | ![Pure Culture Gram-negative bacilli](assets/pure_culture_negbac.png) |
| Clinical Specimen: Gram-positive cocci | ![Clinical Gram-positive cocci](assets/clinical_poscoc.jpg) |
| Clinical Specimen: Gram-negative bacilli | ![Clinical Gram-negative bacilli](assets/clinical_negbac.jpg) |

## Environment Setup

For the full project environment, including notebooks, training scripts, and the
API service:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For API-only usage, install the smaller dependency set:

```powershell
python -m pip install -r 04_model_api\requirements.txt
```

## Model API

The repository includes a FastAPI service for running inference with the saved
`best.pt` checkpoints.

Run the API locally:

```powershell
python -m uvicorn 04_model_api.server:app --reload --host 0.0.0.0 --port 8000
```

Or run it with Docker:

```powershell
docker compose -f 04_model_api/docker-compose.yml up --build
```

Open the Swagger UI at `http://localhost:8000/docs`.

For more options, see [04_model_api/README.md](04_model_api/README.md).
