# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Six-phase single-cell multi-omics analysis of Fezf2-mediated mouse cortical development (GSE153164, Di Bella et al. 2021). All work lives in `notebooks/01_*.ipynb` through `06_*.ipynb`, executed **in order** — each phase reads the AnnData objects written by prior phases. There is no application code or test suite; "the codebase" is the notebooks plus their `.h5ad` outputs.

## Environment & commands

This project uses **uv**, not conda (the `conda` instructions in `README.md`, `docs/setup.md`, and `.github/copilot-instructions.md` are stale — the live env is `.venv/` driven by `pyproject.toml` + `uv.lock`, Python 3.11).

```bash
uv sync                       # install/restore the environment from uv.lock
uv run jupyter lab            # launch Jupyter against the project venv
uv run python <script.py>     # run anything in the env
uv add <pkg>                  # add a dependency (updates pyproject.toml + lock)
```

There is no build, lint, or unit-test step. Validation is done inside the notebooks: shape/type assertions after major steps, checkpoint `.h5ad` writes, figure-existence checks, and cross-dataset validation in Phase 6.

## Phase pipeline (must run sequentially)

| Notebook | Phase | Produces |
|----------|-------|----------|
| `01_preprocessing.ipynb` | QC (MAD-based), Solo doublet detection, Harmony + scVI integration, Leiden clustering | `data/processed/adata_integrated.h5ad` (~125k cells × 21k genes, ~4.7 GB) |
| `02_temporal_analysis.ipynb` | Cell-type annotation, scVelo RNA velocity, PAGA + diffusion pseudotime, time-resolved DE | adds `cell_type`, velocity, pseudotime to adata; 16 figures |
| `03_dose_response.ipynb` | WT→HET→KO dose modeling, sex-specific P1 analysis | gene classification lists; 9 figures |
| `04_multiomics_grn.ipynb` | scRNA+scATAC integration (E13/E15/E18), peak-to-gene, GRN | GRN, Fezf2 direct targets |
| `05_therapeutic_targets.ipynb` | Druggable-gene ID, drug-gene DB queries | ranked target list |
| `06_validation.ipynb` | Cross-validation, publication figures | manuscript figures |

Outputs land in `results/<phase>/`; data objects in `data/processed/`. Note `docs/setup.md` references `phaseN_*` notebook names — the actual files use the `NN_*` numeric prefix above.

## Critical conventions (carry into any new analysis cell)

- **Never run Wilcoxon DE on the full dataset** — it densifies the sparse matrix (~20 GB) and OOMs. Use `sc.tl.rank_genes_groups(..., method='t-test_overestim_var', use_raw=False, pts=True)` (10–100× faster, <4 GB). `logreg` if a multivariate method is needed.
- Keep `adata.X` sparse: `assert scipy.sparse.issparse(adata.X)` before heavy ops; `gc.collect()` after loading/dropping large objects.
- Put `sc.settings.n_jobs = -1` in every notebook's setup cell.
- Figures are **PDF only** (journals require TrueType): `plt.rcParams['pdf.fonttype']=42`, `['ps.fonttype']=42`, then `plt.savefig(..., dpi=300, bbox_inches='tight')`. No PNG for publication output.

## Key data model

- `adata.obs`: `genotype` (all-caps `WT` / `HET` / `KO`), `timepoint` (E10–E18.5, P1, P4), `sex`, `cell_type`, `leiden`, `sample` (the integration `batch_key`).
- `adata.obsm['X_scVI']`: integrated latent space. `adata.uns['rank_genes_*']`: DE results.
- Sex-stratified P1 samples `P1_S1_F` / `P1_S1_M` are **Het** female/male, not WT.
- Config baseline (per `docs/setup.md`): `min_genes=200`, `max_genes=8000`, `max_mito_pct=12`, `n_hvg=3000`, `scvi_latent=50`; species `mmusculus`, genome `mm10`.

## Reference docs

`README.md` (findings overview), `RESEARCH_PLAN.md` (hypotheses), `.github/copilot-instructions.md` (detailed patterns/gotchas — but treat its conda setup as outdated), `docs/internal/PERFORMANCE_FIXES_SUMMARY.md` (why the Wilcoxon→t-test and PDF-font changes were made).
