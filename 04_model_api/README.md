# Model API and Docker Inference

This folder contains deployment-facing files for running inference with the
saved YOLO checkpoints from `03_training_model`.

The current setup is a Dockerized command-line inference image. It uses the
existing `predict_best_model.py` script and includes the saved `best.pt`
checkpoints during image build.

## Files

- `Dockerfile`: builds a CPU-friendly Python image for inference
- `Dockerfile.dockerignore`: keeps the Docker build context small
- `docker-compose.inference.yml`: example compose run on sample images
- `requirements-inference.txt`: minimal Python dependencies for inference

## Build

Run this command from the project root:

```powershell
docker build -f 04_model_api/Dockerfile -t gram-stain-inference .
```

## Run on a Folder of Images

PowerShell:

```powershell
docker run --rm `
  -v "${PWD}\assets:/input:ro" `
  -v "${PWD}\runs\docker_predict:/outputs" `
  gram-stain-inference `
  --model clinical `
  --source /input `
  --project-name /outputs `
  --run-name clinical_assets `
  --exist-ok
```

CMD:

```bat
docker run --rm ^
  -v "%cd%\assets:/input:ro" ^
  -v "%cd%\runs\docker_predict:/outputs" ^
  gram-stain-inference ^
  --model clinical ^
  --source /input ^
  --project-name /outputs ^
  --run-name clinical_assets ^
  --exist-ok
```

Outputs are written to:

```text
runs/docker_predict/clinical_assets
```

## Choose a Model

Use one of the predefined checkpoints:

```powershell
--model pure
--model clinical
```

The default checkpoints are:

```text
03_training_model/pure_culture_weights/best.pt
03_training_model/clinical_specimen_weights/best.pt
```

## Optional Flags

Save YOLO text labels:

```powershell
--save-txt
```

Save confidence values in labels:

```powershell
--save-conf
```

Adjust confidence threshold:

```powershell
--conf 0.35
```

## Docker Compose

Run this command from the project root:

```powershell
docker compose -f 04_model_api/docker-compose.inference.yml up --build
```
