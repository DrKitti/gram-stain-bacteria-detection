# Training Scripts

This folder contains the scripts used for final model preparation and training.

## Files

- `prepare_dataset_configs.py`: creates local `train/val/test` split files and YOLO dataset YAML configs from the dataset folders on the current machine
- `train_final_model.py`: trains `YOLO11m` on `Pure Culture`, `Clinical Specimen`, or both as separate models
- `evaluate_best_model.py`: evaluates the saved `best.pt` checkpoint for `Pure Culture` or `Clinical Specimen`
- `predict_best_model.py`: runs prediction with the saved `best.pt` checkpoint for `Pure Culture` or `Clinical Specimen`

## Recommended Order

1. Place the datasets under `Data/Pure Culture` and `Data/Clinical Specimen`
2. Run `prepare_dataset_configs.py`
3. Run `train_final_model.py`
4. Run `evaluate_best_model.py` or `predict_best_model.py` with the model you want to use

## Example Commands

```powershell
python 3_Training_Model\prepare_dataset_configs.py
python 3_Training_Model\train_final_model.py --dataset both
python 3_Training_Model\evaluate_best_model.py --model pure
python 3_Training_Model\predict_best_model.py --model clinical --source path\to\images
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
- evaluation and prediction scripts let you choose `pure` or `clinical` model directly
- generated split files and YAML configs are local machine outputs, not fixed repository assets
