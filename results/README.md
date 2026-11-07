# Results

Commit small tables and figures. Do not commit raw data or model checkpoints.

## `baseline_metrics.csv`

| column | meaning |
|---|---|
| `model` | LogisticRegression / RandomForest / XGBoost / MLP |
| `endpoint` | Response / OS / PFS |
| `split` | train_cv / test |
| `metric` | auroc / auprc / c_index |
| `value` | point estimate |
| `ci_low` | 95% bootstrap CI lower |
| `ci_high` | 95% bootstrap CI upper |
| `notes` | preprocessing, random seed, caveats |

## `survival_metrics.csv`

| column | meaning |
|---|---|
| `model` | Cox / KM / Transformer |
| `endpoint` | OS / PFS |
| `split` | train / test |
| `c_index` | concordance index |
| `notes` | covariates, censoring notes |

## Figures

- `baseline_roc.png`
- `baseline_calibration.png`
- `km_os.png`
- `training_curve.png`

Always label: model, split, n, metric. A figure without these is not a result.
