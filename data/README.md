# Data

## Public dataset: Chowell 2021

Download with:

```powershell
python src/load_chowell.py
```

Files produced:

- `data/raw/chowell_train.csv` (~1.18k rows)
- `data/raw/chowell_test.csv` (~295 rows)

Columns include:

- `SAMPLE_ID` — ID, not a feature.
- 17 features such as Age, Sex, BMI, Stage, NLR, Platelets, HGB, Albumin, Drug, TMB, FCNA, HED, HLA_LOH, MSI, MSI_SCORE, Chemo_before_IO, Cancer_Type2.
- `Response (1:Responder; 0:Non-responder)` — classification target.
- `OS_Event`, `OS_Months` — overall survival.
- `PFS_Event`, `PFS_Months` — progression-free survival.
- `RF16_prob` — **do not use as a feature**; it is a precomputed model output and would leak the target.

Raw and processed data are excluded from git.

## Own rectal cancer data (from the mentor)

When the data dictionary arrives (target: week 8–10), record:

- Data type: clinical table / bulk RNA-seq / scRNA-seq / WES / pathology / imaging.
- Sample size and number of events.
- Primary endpoint: pCR / TRG / DFS / OS / response.
- Treatment: neoadjuvant chemoradiotherapy? immunotherapy? both?
- Follow-up duration and missingness.
- Ethics approval, de-identification rules, approved storage location.

**Rules:**

- Only process own data on the hospital-approved server/network.
- No patient identifiers on a personal laptop.
- Never upload own data to public cloud, GitHub, or third-party websites.
