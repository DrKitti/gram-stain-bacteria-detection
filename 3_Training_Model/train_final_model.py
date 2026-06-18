from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageFilter


DEFAULT_CONFIGS = {
    "pure": {
        "yaml": Path("Data/pure_culture.yaml"),
        "name": "pure_culture_yolo11m",
    },
    "clinical": {
        "yaml": Path("Data/clinical_specimen.yaml"),
        "name": "clinical_specimen_yolo11m",
    },
}


def parse_simple_yolo_yaml(yaml_path: Path) -> dict[str, str]:
    config: dict[str, str] = {}
    for raw_line in yaml_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in {"path", "train", "val", "test"}:
            config[key] = value
    return config


def read_split_file(split_path: Path) -> list[Path]:
    return [
        Path(line.strip())
        for line in split_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_yolo_label_lines(label_path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 5:
            rows.append(parts)
    return rows


def save_yolo_label_lines(label_path: Path, rows: list[list[str]]) -> None:
    label_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [" ".join(row) for row in rows]
    text = "\n".join(lines)
    if text:
        text += "\n"
    label_path.write_text(text, encoding="utf-8")


def transform_boxes(rows: list[list[str]], mode: str) -> list[list[str]]:
    transformed: list[list[str]] = []
    for row in rows:
        class_id = row[0]
        xc, yc, w, h = map(float, row[1:])

        if mode == "hflip":
            new_xc, new_yc, new_w, new_h = 1.0 - xc, yc, w, h
        elif mode == "vflip":
            new_xc, new_yc, new_w, new_h = xc, 1.0 - yc, w, h
        elif mode == "rot90":
            new_xc, new_yc, new_w, new_h = yc, 1.0 - xc, h, w
        elif mode == "rot180":
            new_xc, new_yc, new_w, new_h = 1.0 - xc, 1.0 - yc, w, h
        elif mode == "rot270":
            new_xc, new_yc, new_w, new_h = 1.0 - yc, xc, h, w
        elif mode == "blur":
            new_xc, new_yc, new_w, new_h = xc, yc, w, h
        else:
            raise ValueError(f"Unsupported augmentation mode: {mode}")

        transformed.append(
            [
                class_id,
                f"{new_xc:.6f}",
                f"{new_yc:.6f}",
                f"{new_w:.6f}",
                f"{new_h:.6f}",
            ]
        )
    return transformed


def apply_image_transform(image: Image.Image, mode: str) -> Image.Image:
    if mode == "hflip":
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if mode == "vflip":
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if mode == "rot90":
        return image.transpose(Image.Transpose.ROTATE_90)
    if mode == "rot180":
        return image.transpose(Image.Transpose.ROTATE_180)
    if mode == "rot270":
        return image.transpose(Image.Transpose.ROTATE_270)
    if mode == "blur":
        return image.filter(ImageFilter.GaussianBlur(radius=0.9))
    raise ValueError(f"Unsupported augmentation mode: {mode}")


def build_augmented_dataset_yaml(
    original_yaml_path: Path,
    new_train_split_path: Path,
) -> Path:
    original_lines = original_yaml_path.read_text(encoding="utf-8").splitlines()
    rewritten_lines = []
    for line in original_lines:
        if line.strip().startswith("train:"):
            rewritten_lines.append(f"train: {new_train_split_path.resolve().as_posix()}")
        else:
            rewritten_lines.append(line)

    augmented_yaml_path = original_yaml_path.with_name(
        f"{original_yaml_path.stem}_augmented{original_yaml_path.suffix}"
    )
    augmented_yaml_path.write_text("\n".join(rewritten_lines) + "\n", encoding="utf-8")
    return augmented_yaml_path


def prepare_augmented_training_inputs(dataset_key: str, yaml_path: Path) -> Path:
    config = parse_simple_yolo_yaml(yaml_path)
    dataset_root = Path(config["path"])
    train_split_path = dataset_root / config["train"]
    train_images = read_split_file(train_split_path)

    labels_dir = dataset_root / "labels"
    augmented_root = dataset_root / "augmented_train"
    augmented_images_dir = augmented_root / "images"
    augmented_labels_dir = augmented_root / "labels"
    augmented_split_path = augmented_root / "train_augmented.txt"

    augmented_images_dir.mkdir(parents=True, exist_ok=True)
    augmented_labels_dir.mkdir(parents=True, exist_ok=True)

    modes = ["hflip", "vflip", "rot90", "rot180", "rot270", "blur"]
    split_lines: list[str] = []

    for image_path in train_images:
        split_lines.append(image_path.resolve().as_posix())

        label_path = labels_dir / f"{image_path.stem}.txt"
        label_rows = load_yolo_label_lines(label_path)
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            for mode in modes:
                transformed_image = apply_image_transform(image, mode)
                transformed_rows = transform_boxes(label_rows, mode)

                out_image_name = f"{image_path.stem}_{mode}{image_path.suffix.lower()}"
                out_label_name = f"{image_path.stem}_{mode}.txt"
                out_image_path = augmented_images_dir / out_image_name
                out_label_path = augmented_labels_dir / out_label_name

                transformed_image.save(out_image_path)
                save_yolo_label_lines(out_label_path, transformed_rows)
                split_lines.append(out_image_path.resolve().as_posix())

    augmented_split_path.write_text("\n".join(split_lines) + "\n", encoding="utf-8")
    print(f"Prepared augmented training split for {dataset_key}: {augmented_split_path}")
    return build_augmented_dataset_yaml(yaml_path, augmented_split_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train final YOLO11m models for Pure Culture and Clinical Specimen."
    )
    parser.add_argument(
        "--dataset",
        choices=["pure", "clinical", "both"],
        default="both",
        help="Which dataset to train.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing the Data folder.",
    )
    parser.add_argument(
        "--model",
        default="yolo11m.pt",
        help="Ultralytics model checkpoint to start from.",
    )
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--max-det", type=int, default=1500)
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Enable dataset caching during training.",
    )
    parser.add_argument(
        "--project-name",
        default="runs/train",
        help="Ultralytics project output directory.",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Training device, for example cpu, 0, or 0,1.",
    )
    parser.add_argument(
        "--disable-augment",
        action="store_true",
        help="Disable custom train-split augmentation before training.",
    )
    return parser.parse_args()


def train_one_dataset(
    dataset_key: str,
    yaml_path: Path,
    run_name: str,
    args: argparse.Namespace,
) -> None:
    from ultralytics import YOLO

    if not yaml_path.exists():
        raise FileNotFoundError(
            f"Dataset config not found for '{dataset_key}': {yaml_path}\n"
            "Run prepare_dataset_configs.py first."
        )

    train_yaml_path = yaml_path
    if not args.disable_augment:
        train_yaml_path = prepare_augmented_training_inputs(dataset_key, yaml_path)

    print(f"\nTraining dataset: {dataset_key}")
    print(f"Using YAML: {train_yaml_path}")
    print(f"Run name: {run_name}")

    model = YOLO(args.model)
    model.train(
        data=str(train_yaml_path),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        max_det=args.max_det,
        cache=args.cache,
        project=args.project_name,
        name=run_name,
        device=args.device,
    )


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()

    dataset_keys = ["pure", "clinical"] if args.dataset == "both" else [args.dataset]

    for dataset_key in dataset_keys:
        config = DEFAULT_CONFIGS[dataset_key]
        yaml_path = (project_root / config["yaml"]).resolve()
        train_one_dataset(
            dataset_key=dataset_key,
            yaml_path=yaml_path,
            run_name=config["name"],
            args=args,
        )


if __name__ == "__main__":
    main()
