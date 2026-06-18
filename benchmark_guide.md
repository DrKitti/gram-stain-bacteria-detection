# Benchmark Model Notebook Guide

This document outlines the structure and objectives of the `02_benchmark_model.ipynb` notebook.

The purpose of this notebook is to analyze and compare previously trained YOLO models using their saved training results. This notebook does not retrain models. Instead, it loads benchmark result files, summarizes model performance, visualizes comparisons, and identifies the best model for further training or deployment.

---

# 1. Benchmark Objective

## Objective

Explain the role of the benchmark process in this project.

## Description

The benchmark process was conducted to compare multiple YOLO-based object detection models and select the most suitable architecture for Gram-stained bacteria detection.

The evaluated models include:

* YOLOv8n
* YOLOv8s
* YOLOv8m
* YOLOv11n
* YOLOv11s
* YOLOv11m

## Key Questions

* Which model achieves the best detection performance?
* Which model provides the best trade-off between accuracy and efficiency?
* Which architecture should be selected for final training?

---

# 2. Load Benchmark Results

## Objective

Load saved training result files from each model.

## Expected Input Files

```text
results/benchmark/
├── yolov8n_results.csv
├── yolov8s_results.csv
├── yolov8m_results.csv
├── yolov11n_results.csv
├── yolov11s_results.csv
└── yolov11m_results.csv
```

## Notes

These CSV files are exported from previous YOLO training runs.

The notebook should not depend on Google Drive or local machine-specific paths. All required benchmark CSV files should be copied into the repository under `results/benchmark/`.

---

# 3. Extract Final or Best Epoch Metrics

## Objective

Extract comparable metrics from each model result file.

## Suggested Metrics

* mAP@50
* mAP@50-95
* Precision
* Recall
* F1-score
* Training loss
* Validation loss

## Suggested Approach

For each model, extract either:

1. The best epoch based on mAP@50-95, or
2. The final epoch if the training strategy requires final checkpoint comparison.

## Recommended Selection Rule

Use the epoch with the highest validation mAP@50-95 as the representative benchmark result.

## Output

Create a combined benchmark table:

| Model    | Best Epoch | mAP@50 | mAP@50-95 | Precision | Recall | F1  |
| -------- | ---------- | ------ | --------- | --------- | ------ | --- |
| YOLOv8n  | xxx        | xxx    | xxx       | xxx       | xxx    | xxx |
| YOLOv8s  | xxx        | xxx    | xxx       | xxx       | xxx    | xxx |
| YOLOv8m  | xxx        | xxx    | xxx       | xxx       | xxx    | xxx |
| YOLOv11n | xxx        | xxx    | xxx       | xxx       | xxx    | xxx |
| YOLOv11s | xxx        | xxx    | xxx       | xxx       | xxx    | xxx |
| YOLOv11m | xxx        | xxx    | xxx       | xxx       | xxx    | xxx |

---

# 4. Save Combined Benchmark Summary

## Objective

Save a clean benchmark summary file for reuse in README and reports.

## Output File

```text
results/benchmark_metrics.csv
```

## Purpose

This file should act as the main benchmark result table for:

* README table
* Result visualization
* Project documentation
* Model selection decision

---

# 5. Visualize Model Comparison

## Objective

Create visual comparisons across all benchmarked models.

## Suggested Visualizations

### mAP@50 Comparison

Bar chart comparing model detection performance.

### mAP@50-95 Comparison

Bar chart comparing stricter detection performance.

### Precision and Recall Comparison

Grouped bar chart or line plot.

### F1-score Comparison

Bar chart showing balanced detection performance.

### Optional Speed Comparison

If available:

* Inference time
* FPS
* Model size
* Parameter count

## Key Questions

* Does YOLOv11 outperform YOLOv8?
* Does a larger model always perform better?
* Which model provides the best practical trade-off?

---

# 6. Training Curve Analysis

## Objective

Analyze model learning behavior during training.

## Suggested Visualizations

For each model or selected top models:

* mAP@50-95 over epochs
* Precision over epochs
* Recall over epochs
* Training loss over epochs
* Validation loss over epochs

## Key Questions

* Did the model converge?
* Is there evidence of overfitting?
* Which model trained more stably?

---

# 7. Best Model Selection

## Objective

Select the best model for final training and practical use.

## Selection Criteria

The best model should be selected based on:

* mAP@50-95
* Precision
* Recall
* F1-score
* Model size
* Inference speed
* Practical deployment constraints

## Suggested Output

| Selected Model | Reason                                         |
| -------------- | ---------------------------------------------- |
| YOLOvXX        | Best trade-off between accuracy and efficiency |

## Example Discussion

Although one model may achieve the highest mAP, a smaller model may be more suitable for deployment if it provides similar performance with lower computational cost.

---

# 8. Benchmark Discussion

## Objective

Summarize the benchmark findings.

## Suggested Discussion Points

* Best-performing model
* Difference between YOLOv8 and YOLOv11
* Effect of model size
* Accuracy-efficiency trade-off
* Limitations of the benchmark
* Reason for selecting the final model

## Example Findings

* YOLOv11 achieved stronger overall detection performance than YOLOv8.
* Medium-sized models improved accuracy but required more computational resources.
* The selected model was chosen based on both detection performance and practical usability.
* Benchmark results were used as a model selection step before final training.

---

# 9. Deliverables

The notebook should produce:

* Combined benchmark metrics table
* `results/benchmark_metrics.csv`
* Performance comparison charts
* Training curve visualizations
* Best model selection summary
* Final benchmark discussion

The notebook should serve as the main evidence for why a specific YOLO model was selected for final model development.
