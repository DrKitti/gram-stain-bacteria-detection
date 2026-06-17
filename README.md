# Gram Stain Bacteria Detection

A Senior Project on object detection of Gram-stained bacteria from microscope images.

## Project Overview

This project studies automated detection of bacteria in Gram-stained microscopic images using four clinically relevant categories:

- Gram-negative cocci
- Gram-positive cocci
- Gram-negative bacilli
- Gram-positive bacilli

The main goal is to build a detection pipeline that can localize bacteria and classify them into these four groups across two domains:

- `Pure Culture`, which provides cleaner species-based microscope images that were regrouped into Gram-stain categories
- `Clinical Specimen`, which provides more realistic and visually complex images from clinical samples

The project is currently organized into three main parts:

- **Part 1 : Data analysis** for dataset exploration, class distribution study, and Gram-stain bacteria characteristics
- **Part 2 : Benchmark model** for comparing baseline object detection models on the prepared datasets
- **Part 3 : Training model** for developing and improving the final bacteria detection pipeline


## Dataset Summary

The repository currently uses two dataset sources:

- `Pure Culture`: regrouped from public species-level bacteria image datasets
- `Clinical Specimen`: annotated clinical detection dataset used as the main real-world source

More detailed dataset notes, source links, and full example images are available in [data.md](data.md).

## Dataset Preview

| Dataset | Example |
| --- | --- |
| Pure Culture: Gram-positive cocci | ![Pure Culture Gram-positive cocci](assets/pure_culture_poscoc.png) |
| Pure Culture: Gram-negative bacilli | ![Pure Culture Gram-negative bacilli](assets/pure_culture_negbac.png) |
| Clinical Specimen: Gram-positive cocci | ![Clinical Gram-positive cocci](assets/clinical_poscoc.jpg) |
| Clinical Specimen: Gram-negative bacilli | ![Clinical Gram-negative bacilli](assets/clinical_negbac.jpg) |
