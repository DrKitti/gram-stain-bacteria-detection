from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_MODELS = {
    "pure": Path("03_training_model/pure_culture_weights/best.pt"),
    "clinical": Path("03_training_model/clinical_specimen_weights/best.pt"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run prediction with the best Pure Culture or Clinical Specimen model."
    )
    parser.add_argument(
        "--model",
        choices=["pure", "clinical"],
        required=True,
        help="Which predefined best model to use.",
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="Optional explicit path to a model checkpoint. Overrides the predefined weights path.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to an image, folder, or other Ultralytics-supported prediction source.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing the model weights.",
    )
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.7)
    parser.add_argument("--max-det", type=int, default=1500)
    parser.add_argument("--device", default=None, help="Prediction device, for example cpu or 0.")
    parser.add_argument(
        "--save-txt",
        action="store_true",
        help="Save YOLO-format prediction labels.",
    )
    parser.add_argument(
        "--save-conf",
        action="store_true",
        help="Save confidence values in text predictions.",
    )
    parser.add_argument(
        "--project-name",
        default="runs/predict",
        help="Ultralytics project output directory.",
    )
    parser.add_argument(
        "--run-name",
        default=None,
        help="Optional run name. Defaults to <model>_predict.",
    )
    parser.add_argument(
        "--exist-ok",
        action="store_true",
        help="Allow reuse of an existing prediction output directory.",
    )
    return parser.parse_args()


def resolve_weights(args: argparse.Namespace) -> Path:
    project_root = args.project_root.resolve()
    weights_path = (args.weights or (project_root / DEFAULT_MODELS[args.model])).resolve()
    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found: {weights_path}")
    return weights_path


def main() -> None:
    args = parse_args()
    weights_path = resolve_weights(args)
    source_path = args.source.resolve()

    if not source_path.exists():
        raise FileNotFoundError(f"Prediction source not found: {source_path}")

    from ultralytics import YOLO

    run_name = args.run_name or f"{args.model}_predict"

    print(f"Predicting with model: {args.model}")
    print(f"Weights: {weights_path}")
    print(f"Source: {source_path}")

    model = YOLO(str(weights_path))
    results = model.predict(
        source=str(source_path),
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        max_det=args.max_det,
        device=args.device,
        project=args.project_name,
        name=run_name,
        save=True,
        save_txt=args.save_txt,
        save_conf=args.save_conf,
        exist_ok=args.exist_ok,
    )

    print(f"Prediction completed on {len(results)} input item(s).")
    print(f"Outputs saved under: {Path(args.project_name) / run_name}")


if __name__ == "__main__":
    main()
