"""Week 0: download the Chowell 2021 dataset and save train/test CSVs.

Run:
    python src/load_chowell.py

The dataset is public:
    https://huggingface.co/datasets/gabrielaltay/chowell-2021

Expected size: ~1.18k train / ~295 test rows, 17 features + outcomes.
"""

from pathlib import Path

import pandas as pd
from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# The 17 features used by the paper's Chowell analysis.
# Do NOT add RF16_prob: it is a precomputed model output (leakage).
FEATURES = [
    "Age",
    "Sex (1:Male; 0:Female)",
    "BMI",
    "Stage (1:IV; 0:I-III)",
    "NLR",
    "Platelets",
    "HGB",
    "Albumin",
    "Drug (1:Combo; 0:PD1/PDL1orCTLA4)",
    "TMB",
    "FCNA",
    "HED",
    "HLA_LOH",
    "MSI (1:Unstable; 0:Stable_Indeterminate)",
    "MSI_SCORE",
    "Chemo_before_IO (1:Yes; 0:No)",
    "Cancer_Type2",
]

TARGETS = [
    "Response (1:Responder; 0:Non-responder)",
    "OS_Event",
    "PFS_Event",
]


def main() -> None:
    ds = load_dataset("gabrielaltay/chowell-2021")
    print(ds)

    for split in ds:
        df = ds[split].to_pandas()
        out = RAW / f"chowell_{split}.csv"
        df.to_csv(out, index=False)

        print(f"\n=== {split} ===")
        print("shape:", df.shape)
        print("columns:", list(df.columns))

        print("\nTop missing values:")
        print(df.isna().sum().sort_values(ascending=False).head(10).to_string())

        for target in TARGETS:
            if target in df.columns:
                print(f"\n{target}:")
                print(df[target].value_counts(dropna=False).to_string())

        print(f"\nSaved -> {out}")

    print("\nFeature list (17):")
    for i, feature in enumerate(FEATURES, start=1):
        print(f"{i:2d}. {feature}")

    print(
        "\nWarning: do NOT use 'RF16_prob' as a feature. "
        "It is a precomputed model output and would leak the target."
    )


if __name__ == "__main__":
    main()
