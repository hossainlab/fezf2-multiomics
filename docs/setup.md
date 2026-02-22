## Project Overview

Multi-omics single-cell analysis of Fezf2-mediated cortical development in mouse. Investigates how Fezf2 mutations disrupt brain cortical development using integrated scRNA-seq and scATAC-seq data from the GSE153164 dataset (Di Bella et al. 2021).

**Dataset**: 23 scRNA-seq samples (E10-P4) + 3 scATAC-seq samples (E13.5, E15.5, E18.5) with WT/Het/KO genotypes.

## Environment Setup

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate scverse

# Launch Jupyter for analysis
jupyter lab
```

**Python 3.11** with scverse ecosystem: scanpy, anndata, scvi-tools, muon, cellrank, decoupler, pertpy.

## Project Structure

```
notebooks/           # Phase-based Jupyter notebooks (execute in order)
  phase1_preprocessing.ipynb      # QC, integration, clustering
  phase2_temporal_analysis.ipynb  # Cell annotation, velocity, trajectories
  phase3_dose_response.ipynb      # WT/Het/KO comparisons, dose-response
  phase4_multiomics_grn.ipynb     # ATAC integration, GRN reconstruction
  phase5_therapeutic_targets.ipynb # Druggable target identification
  phase6_validation_manuscript.ipynb # Validation, figures
data/
  scRNAseq/          # h5 files per sample
  scATACseq/         # Peak matrices
results/             # Outputs organized by phase (figures/, tables/)
config.yml           # Central configuration for all parameters
```

## Configuration

All analysis parameters are centralized in `config.yml`:
- QC thresholds: min_genes=200, max_genes=8000, max_mito_pct=12
- Integration: n_hvg=3000, scvi_latent=50, batch_key="sample"
- Species: mmusculus, genome: mm10

## Analysis Pipeline Architecture

The 6-phase pipeline builds sequentially, with each phase reading outputs from prior phases:

**Phase 1** → Creates `adata_integrated.h5ad` (main integrated object ~4.7GB)
**Phase 2** → Adds cell type annotations, velocity, pseudotime to adata
**Phase 3** → Dose-response analysis, gene classifications
**Phase 4** → Multi-omics integration, GRN reconstruction
**Phase 5** → Therapeutic target prioritization
**Phase 6** → Publication figures and validation

## Critical Technical Notes

### Memory Management
- **Never use Wilcoxon** for DE on full dataset - causes ~20GB memory allocation failure
- Use `method='t-test_overestim_var'` for `sc.tl.rank_genes_groups()` (10-100x faster, works with sparse)
- Keep data sparse: `assert scipy.sparse.issparse(adata.X)`

### Performance Settings
```python
sc.settings.n_jobs = -1  # Parallel processing
```

### Publication Figures
```python
plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts
plt.rcParams['ps.fonttype'] = 42
# Save as PDF, not PNG
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

## Key Data Objects

- **adata**: Main AnnData object with ~125k cells
- **adata.obs**: Sample metadata (genotype, timepoint, sex, cell_type)
- **adata.obsm['X_scVI']**: Integrated latent representation
- **adata.uns['rank_genes_*']**: Differential expression results

## Genotype/Condition Mapping

Per `config.yml`:
- Fezf2KO → KO genotype
- Fezf2Het → HET genotype
- WT, P1_S1, P1_S2 → WT genotype
- P1F/P1M suffixes → sex-stratified Het samples
