from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MODELS = {
    "pure": {
        "weights": Path("03_training_model/pure_culture_weights/best.pt"),
        "yaml": Path("Data/pure_culture.yaml"),
    },
    "clinical": {
        "weights": Path("03_training_model/clinical_specimen_weights/best.pt"),
        "yaml": Path("Data/clinical_specimen.yaml"),
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate the best YOLO model for Pure Culture or Clinical Specimen."
    )
    parser.add_argument(
        "--model",
        choices=["pure", "clinical"],
        required=True,
        help="Which predefined best model to evaluate.",
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="Optional explicit path to a model checkpoint. Overrides the predefined weights path.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Optional explicit path to a dataset YAML file. Overrides the predefined yaml path.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing the Data folder.",
    )
    parser.add_argument("--split", choices=["val", "test"], default="test")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.7)
    parser.add_argument("--max-det", type=int, default=1500)
    parser.add_argument("--device", default=None, help="Evaluation device, for example cpu or 0.")
    parser.add_argument(
        "--save-json",
        action="store_true",
        help="Save COCO-style prediction JSON if supported by the dataset/task.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to save a compact evaluation summary as JSON.",
    )
    return parser.parse_args()


def resolve_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    project_root = args.project_root.resolve()
    default_config = DEFAULT_MODELS[args.model]
    weights_path = (args.weights or (project_root / default_config["weights"])).resolve()
    data_yaml = (args.data or (project_root / default_config["yaml"])).resolve()

    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found: {weights_path}")
    if not data_yaml.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {data_yaml}")
    return weights_path, data_yaml


def metrics_to_summary(metrics, model_name: str, weights_path: Path, data_yaml: Path, split: str) -> dict:
    box = metrics.box
    return {
        "model": model_name,
        "weights": str(weights_path),
        "data_yaml": str(data_yaml),
        "split": split,
        "precision": float(box.mp),
        "recall": float(box.mr),
        "map50": float(box.map50),
        "map50_95": float(box.map),
        "class_map50_95": [float(x) for x in box.maps],
    }


def main() -> None:
    args = parse_args()
    weights_path, data_yaml = resolve_paths(args)

    from ultralytics import YOLO

    print(f"Evaluating model: {args.model}")
    print(f"Weights: {weights_path}")
    print(f"Dataset YAML: {data_yaml}")
    print(f"Split: {args.split}")

    model = YOLO(str(weights_path))
    metrics = model.val(
        data=str(data_yaml),
        split=args.split,
        imgsz=args.imgsz,
        batch=args.batch,
        conf=args.conf,
        iou=args.iou,
        max_det=args.max_det,
        device=args.device,
        save_json=args.save_json,
    )

    summary = metrics_to_summary(metrics, args.model, weights_path, data_yaml, args.split)
    print(json.dumps(summary, indent=2))

    if args.output_json is not None:
        output_json = args.output_json.resolve()
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Saved evaluation summary to: {output_json}")


if __name__ == "__main__":
    main()
