# Training Scripts

This folder contains the scripts used for final model preparation and training.

## Files

- `prepare_dataset_configs.py`: creates local `train/val/test` split files and YOLO dataset YAML configs from the dataset folders on the current machine
- `train_final_model.py`: trains `YOLO11m` on `Pure Culture`, `Clinical Specimen`, or both as separate models

## Recommended Order

1. Place the datasets under `Data/Pure Culture` and `Data/Clinical Specimen`
2. Run `prepare_dataset_configs.py`
3. Run `train_final_model.py`

## Example Commands

```powershell
python 3_Training_Model\prepare_dataset_configs.py
python 3_Training_Model\train_final_model.py --dataset both
```

## Augmentation

Custom augmentation is applied to the `train` split only:

- horizontal flip
- vertical flip
- rotation `90` degrees
- rotation `180` degrees
- rotation `270` degrees
- Gaussian blur with radius `0.9`

Validation and test splits are not augmented.

## Notes

- `Pure Culture` and `Clinical Specimen` are trained as separate models
- `YOLO11m` starts from `yolo11m.pt` from Ultralytics
- generated split files and YAML configs are local machine outputs, not fixed repository assets
