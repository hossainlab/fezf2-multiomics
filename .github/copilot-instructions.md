# Copilot Instructions for Fezf2 Multi-Omics Single-Cell Analysis

This is a **Jupyter notebook-based Jupyter-centric single-cell analysis pipeline** investigating Fezf2-mediated cortical development using scRNA-seq and scATAC-seq data from GEO GSE153164 (Di Bella et al. 2021).

## Quick Setup

```bash
# Environment setup
conda env create -f envs/environment.yml
conda activate scverse

# Run analysis
jupyter lab
# Execute notebooks in order: 01_preprocessing.ipynb → 06_validation.ipynb
```

**Key Requirements:**
- Python 3.11
- RAM: ≥128 GB (integrated object ~4.67 GB, but analysis needs headroom)
- Storage: ~500 GB for data and intermediates

## Project Architecture

### Six-Phase Sequential Pipeline
The analysis is organized into phases that must execute **in order** (each reads outputs from prior phases):

1. **Phase 1: Preprocessing** (`01_preprocessing.ipynb`)
   - QC (MAD-based adaptive thresholding for genes, UMI, mitochondrial %)
   - Deep learning doublet detection (Solo via scvi-tools)
   - Batch integration (Harmony + scVI)
   - Outputs: `adata_integrated.h5ad` (~125k cells × 21k genes, 4.67 GB)

2. **Phase 2: Temporal Analysis** (`02_temporal_analysis.ipynb`)
   - Cell type annotation with marker gene scoring
   - RNA velocity (scVelo) and trajectory inference (PAGA, diffusion pseudotime)
   - Time-resolved DE analysis across genotypes
   - Outputs: 16 publication-quality figures

3. **Phase 3: Dose-Response** (`03_dose_response.ipynb`)
   - Gene dosage modeling (WT → Het → KO)
   - Classification: 7,248 genes show linear dose-response, 13,782 show no response
   - Sex-specific analysis at P1
   - Outputs: 9 figures, gene classification lists

4. **Phase 4: Multi-Omics & GRN** (`04_multiomics_grn.ipynb`)
   - Integrate scRNA-seq + scATAC-seq at matched timepoints (E13, E15, E18)
   - Peak-to-gene linkage, TF motif enrichment
   - Gene regulatory network reconstruction
   - Outputs: GRN, Fezf2 direct targets

5. **Phase 5: Therapeutic Targets** (`05_therapeutic_targets.ipynb`)
   - Druggable gene identification (GPCRs, kinases, epigenetic modifiers)
   - Drug-gene interaction queries (DGIdb, ChEMBL)
   - Outputs: Ranked therapeutic target list

6. **Phase 6: Validation & Figures** (`06_validation.ipynb`)
   - Cross-validation with published datasets
   - Publication-ready figure generation
   - Outputs: 56 manuscript-quality figures

### Data Objects & Storage
- **Main object**: `adata` — AnnData object with ~125k cells
- **Key slots**:
  - `adata.obs`: Sample metadata (genotype, timepoint, sex, cell_type)
  - `adata.obsm['X_scVI']`: Integrated latent representation
  - `adata.uns['rank_genes_*']`: DE results
- **Genotype mapping**: WT / HET (Fezf2Het) / KO (Fezf2KO)
- **Timepoints**: E10–E18.5, P1, P4

## Performance & Memory Critical Notes

### ⚠️ Differential Expression Methods
**NEVER use Wilcoxon for DE on full dataset** — it converts sparse matrices to dense, requiring ~19.7 GB for 125k cells × 21k genes.

**Use this instead:**
```python
sc.tl.rank_genes_groups(
    adata,
    groupby='cell_type',
    method='t-test_overestim_var',  # ✅ 10-100x faster, <4 GB RAM
    use_raw=False,
    pts=True  # Include percentage of cells expressing gene
)
```

**Alternative (if multivariate preferred)**: `method='logreg'`

### Memory Management Best Practices
```python
# 1. Verify sparsity is preserved
import scipy.sparse as sp
assert sp.issparse(adata.X)

# 2. Enable parallel processing
sc.settings.n_jobs = -1  # Must be in every notebook's setup cell

# 3. Monitor memory if needed
import psutil
print(f"Available: {psutil.virtual_memory().available / 1e9:.1f} GB")
```

### Publication Figure Settings
All notebooks should include this in their setup cell (after `sc.settings.set_figure_params()`):

```python
# Set publication-ready matplotlib parameters
plt.rcParams['pdf.fonttype'] = 42    # TrueType fonts (required by journals)
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['figure.titlesize'] = 16

# Always save as PDF, not PNG
plt.savefig(output_path / 'figure_name.pdf', dpi=300, bbox_inches='tight')
```

## Key Conventions & Patterns

### Clustering & Cell Type Keys
- **Leiden clustering key**: `'leiden'` (default in Phase 1)
- **Cell type annotation key**: `'cell_type'` (added in Phase 2)
- **Batch key**: `'sample'` (crucial for integration methods)

### Result Storage
- Differential expression results stored in `adata.uns['rank_genes_*']` with keys like `'scores'`, `'logfoldchanges'`, `'pvals'`
- Trajectory/pseudotime results in `adata.obs` columns (e.g., `adata.obs['dpt_pseudotime']`)
- PAGA results in `adata.uns['paga']`

### File Naming Conventions
- **Notebooks**: `NN_phase_description.ipynb` (e.g., `04_multiomics_grn.ipynb`)
- **Output figures**: `NN_figure_description.pdf` (e.g., `02_celltype_scores_umap.pdf`)
- **Data objects**: `adata_purpose.h5ad` (e.g., `adata_integrated.h5ad`)

### Common Imports (Expected in Every Notebook)
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import scvelo as scv  # Phase 2 onwards
from pathlib import Path
import gc
```

## Config File Reference
Check `docs/setup.md` for:
- QC thresholds (min_genes=200, max_genes=8000, max_mito_pct=12)
- Integration parameters (n_hvg=3000, scvi_latent=50)
- Species/genome info (mm10, mmusculus)

## Tools & Libraries

**Core Framework**: Scanpy, AnnData, Muon (multi-omics)
**Integration**: Harmony, scVI
**Dynamics**: scVelo (RNA velocity), CellRank, PAGA
**GRN**: Decoupler, SCENIC
**Statistics**: Scipy, Statsmodels, Scikit-learn
**Visualization**: Matplotlib, Seaborn
**Deep Learning**: PyTorch, PyTorch Lightning, JAX/Flax

## Documentation References

- **Setup**: `docs/setup.md` (environment, parameters, genotype mapping)
- **Performance Details**: `docs/internal/PERFORMANCE_FIXES_SUMMARY.md` (optimization patterns)
- **Research Plan**: `RESEARCH_PLAN.md` (hypotheses, expected findings)
- **README**: High-level overview and key findings

## Running Tests/Validation

This is primarily a research notebook project, so testing is done through:
1. **Intermediate checkpoint validation** — Save `adata_checkpoint.h5ad` after major steps
2. **Figure existence checks** — Verify PDFs are generated in expected paths
3. **Data shape/type assertions** — Confirm expected cell/gene counts at each phase
4. **Cross-validation** — Phase 6 includes validation against published datasets

Example checkpoint pattern:
```python
# After DE analysis
adata.write_h5ad(Path('data/processed/adata_after_de.h5ad'), compression='gzip')

# Before Phase 2
adata = sc.read_h5ad('data/processed/adata_integrated.h5ad')
assert adata.n_obs > 120000, "Cells lost in QC!"
assert 'leiden' in adata.obs, "Clustering missing!"
```

## Common Gotchas

1. **Wilcoxon OOM**: Use t-test instead (see Performance section)
2. **Figure format**: Always PDF for publications, not PNG
3. **Batch effects**: Must specify `batch_key='sample'` in integration methods
4. **Memory cleanup**: Call `gc.collect()` after loading/processing large objects
5. **Sparse matrix conversion**: Any dense operation (like density plotting) should be explicit, not accidental
6. **Sex-specific P1 samples**: Named `P1_S1_F` (female) and `P1_S1_M` (male) — these are Het females/males, not WT
7. **Genotype abbreviations**: WT / HET / KO (all caps in `adata.obs['genotype']`)

## Adding New Analysis

Before adding new cells to notebooks:
1. **Check Phase order** — Are dependencies available?
2. **Memory estimate** — Will it fit with sparse matrices?
3. **Output format** — Save as PDF, not PNG
4. **Settings** — Include `sc.settings.n_jobs = -1` in setup cell
5. **Checkpoint** — Save intermediate `adata_*.h5ad` files for reproducibility

## Quick Commands

```bash
# Start Jupyter
jupyter lab

# Read a checkpoint
import scanpy as sc
adata = sc.read_h5ad('data/processed/adata_integrated.h5ad')

# List available metadata
print(adata.obs.columns)  # See available annotations
print(adata.obs['genotype'].value_counts())  # Check genotype distribution
print(f"Cells: {adata.n_obs}, Genes: {adata.n_vars}")

# Enable performance monitoring
sc.settings.n_jobs = -1
import psutil; psutil.cpu_percent()
```

## Links to Key Docs

- **GEO Dataset**: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153164
- **Scanpy Docs**: https://scanpy.readthedocs.io
- **scVelo Docs**: https://scvelo.readthedocs.io
- **CellRank Docs**: https://cellrank.readthedocs.io

---

**Last Updated**: 2025-03 | **Notebook Phases**: 6 | **Dataset**: GSE153164 (125k cells)
