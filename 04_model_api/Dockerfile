FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY 04_model_api/requirements-inference.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements-inference.txt

COPY 03_training_model ./03_training_model

RUN mkdir -p /input /outputs

ENTRYPOINT ["python", "03_training_model/predict_best_model.py"]
CMD ["--help"]
