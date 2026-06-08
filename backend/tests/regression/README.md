# EKA regression suite

## Corpus (50 PDFs)

| Group | Count | Purpose |
|-------|-------|---------|
| Unique topics | 15 | HR, finance, engineering, security, etc. |
| Size variants | 15 | Same fact in short / medium / long bodies (5 topics × 3) |
| Edge cases | 20 | Resumes, portfolio, duplicates, cross-refs, dense facts |

## Run

```bash
cd backend
pip install -r requirements-dev.txt

# In-process (recommended; sync embed, no worker required)
python -m tests.regression.run_regression

# Against running uvicorn on :8000
python -m tests.regression.run_regression --external

# Reuse indexed docs in an existing org
python -m tests.regression.run_regression --email you@example.com --password '...' --skip-upload
```

Report: `tests/regression/REGRESSION_REPORT.md`

## Large PDF benchmark (10 × 200–300 pages, 100 questions)

Validates answers against **ground-truth KEY_FACT lines** in the original PDFs.

```bash
# Full benchmark (~1–3+ hours depending on CPU/API; sync embed)
python -m tests.regression.run_large_regression --pages 250

# Against running uvicorn
python -m tests.regression.run_large_regression --pages 250 --external
```

Report: `tests/regression/LARGE_REGRESSION_REPORT.md`

## Unit tests

```bash
pytest tests/regression/test_corpus_size.py tests/regression/test_corpus_large.py -v
```
