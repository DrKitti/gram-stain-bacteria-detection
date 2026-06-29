from __future__ import annotations

import argparse
import random
from collections import defaultdict
from pathlib import Path


CLASS_NAMES = {
    0: "Gram-negative cocci",
    1: "Gram-positive cocci",
    2: "Gram-negative bacilli",
    3: "Gram-positive bacilli",
}

PURE_PREFIX_TO_CLASS = {
    "negative_cocci": 0,
    "positive_cocci": 1,
    "negative_bacilli": 2,
    "positive_bacilli": 3,
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate local YOLO split files and dataset YAML configs."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing the Data folder.",
    )
    parser.add_argument(
        "--pure-root",
        type=Path,
        default=None,
        help="Path to the Pure Culture dataset root.",
    )
    parser.add_argument(
        "--clinical-root",
        type=Path,
        default=None,
        help="Path to the Clinical Specimen dataset root.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for splitting.")
    parser.add_argument("--train-ratio", type=float, default=0.7, help="Train split ratio.")
    parser.add_argument("--val-ratio", type=float, default=0.2, help="Validation split ratio.")
    parser.add_argument("--test-ratio", type=float, default=0.1, help="Test split ratio.")
    return parser.parse_args()


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines)
    if text:
        text += "\n"
    path.write_text(text, encoding="utf-8")


def list_images(images_dir: Path) -> list[Path]:
    return sorted(
        p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def split_group(
    files: list[Path],
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
) -> dict[str, list[Path]]:
    total = len(files)
    n_train = round(total * train_ratio)
    n_val = round(total * val_ratio)
    n_test = total - n_train - n_val

    if total >= 3 and n_test < 1:
        n_test = 1
        if n_train >= n_val and n_train > 1:
            n_train -= 1
        elif n_val > 1:
            n_val -= 1
    if total >= 2 and n_val < 1:
        n_val = 1
        if n_train > 1:
            n_train -= 1
        elif n_test > 1:
            n_test -= 1

    return {
        "train": files[:n_train],
        "val": files[n_train : n_train + n_val],
        "test": files[n_train + n_val : n_train + n_val + n_test],
    }


def create_pure_splits(
    pure_root: Path,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> dict[str, int]:
    images_dir = pure_root / "images"
    splits_dir = pure_root / "splits"
    rng = random.Random(seed)

    class_groups: dict[str, list[Path]] = defaultdict(list)
    for image_path in list_images(images_dir):
        prefix = image_path.stem.split("__")[0]
        if prefix not in PURE_PREFIX_TO_CLASS:
            raise ValueError(f"Unknown Pure Culture class prefix: {prefix}")
        class_groups[prefix].append(image_path)

    buckets = {"train": [], "val": [], "test": []}
    for _, files in sorted(class_groups.items()):
        shuffled = files[:]
        rng.shuffle(shuffled)
        split_files = split_group(shuffled, train_ratio, val_ratio, test_ratio)
        for split_name, split_items in split_files.items():
            buckets[split_name].extend(split_items)

    counts = {}
    for split_name, files in buckets.items():
        lines = [path.resolve().as_posix() for path in sorted(files)]
        write_lines(splits_dir / f"{split_name}.txt", lines)
        counts[split_name] = len(lines)
    return counts


def rebuild_clinical_split_from_original(clinical_root: Path, split_name: str) -> list[str]:
    original_txt = clinical_root / "txt" / f"{split_name}.txt"
    images_dir = clinical_root / "images"

    if not original_txt.exists():
        return []

    lines = []
    for raw_line in original_txt.read_text(encoding="utf-8").splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        filename = Path(raw_line).name
        local_image = images_dir / filename
        if local_image.exists():
            lines.append(local_image.resolve().as_posix())
    return lines


def create_random_clinical_splits(
    clinical_root: Path,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> dict[str, list[str]]:
    images_dir = clinical_root / "images"
    image_files = list_images(images_dir)
    rng = random.Random(seed)
    shuffled = image_files[:]
    rng.shuffle(shuffled)
    split_files = split_group(shuffled, train_ratio, val_ratio, test_ratio)
    return {
        split_name: [path.resolve().as_posix() for path in sorted(paths)]
        for split_name, paths in split_files.items()
    }


def create_clinical_splits(
    clinical_root: Path,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> dict[str, int]:
    splits_dir = clinical_root / "splits"

    split_lines = {
        split_name: rebuild_clinical_split_from_original(clinical_root, split_name)
        for split_name in ("train", "val", "test")
    }

    if not all(split_lines.values()):
        split_lines = create_random_clinical_splits(
            clinical_root, train_ratio, val_ratio, test_ratio, seed
        )

    counts = {}
    for split_name, lines in split_lines.items():
        write_lines(splits_dir / f"{split_name}.txt", lines)
        counts[split_name] = len(lines)
    return counts


def write_yaml(dataset_root: Path, yaml_path: Path) -> None:
    lines = [
        f"# YOLO dataset config for {dataset_root.name}",
        f"path: {dataset_root.resolve().as_posix()}",
        "train: splits/train.txt",
        "val: splits/val.txt",
        "test: splits/test.txt",
        "names:",
    ]
    lines.extend(f"  {class_id}: {class_name}" for class_id, class_name in CLASS_NAMES.items())
    yaml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()

    ratio_sum = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(ratio_sum - 1.0) > 1e-9:
        raise ValueError("train-ratio + val-ratio + test-ratio must equal 1.0")

    project_root = args.project_root.resolve()
    pure_root = (args.pure_root or (project_root / "Data" / "Pure Culture")).resolve()
    clinical_root = (args.clinical_root or (project_root / "Data" / "Clinical Specimen")).resolve()

    if not pure_root.exists():
        raise FileNotFoundError(f"Pure Culture root not found: {pure_root}")
    if not clinical_root.exists():
        raise FileNotFoundError(f"Clinical Specimen root not found: {clinical_root}")

    pure_counts = create_pure_splits(
        pure_root,
        args.train_ratio,
        args.val_ratio,
        args.test_ratio,
        args.seed,
    )
    clinical_counts = create_clinical_splits(
        clinical_root,
        args.train_ratio,
        args.val_ratio,
        args.test_ratio,
        args.seed,
    )

    pure_yaml = project_root / "Data" / "pure_culture.yaml"
    clinical_yaml = project_root / "Data" / "clinical_specimen.yaml"
    write_yaml(pure_root, pure_yaml)
    write_yaml(clinical_root, clinical_yaml)

    print("Generated dataset configs successfully.")
    print(f"Pure Culture splits: {pure_counts}")
    print(f"Clinical Specimen splits: {clinical_counts}")
    print(f"Pure Culture YAML: {pure_yaml}")
    print(f"Clinical Specimen YAML: {clinical_yaml}")


if __name__ == "__main__":
    main()
