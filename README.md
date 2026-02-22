# Fezf2-Mediated Cortical Development: Multi-Omics Single-Cell Analysis

## Project Overview

A comprehensive multi-omics analysis of Fezf2-mediated cortical development using the GSE153164 dataset (Di Bella et al. 2021). This project investigates temporal and cell-type-specific mechanisms by which Fezf2 mutations disrupt cortical development across the full E10-P4 developmental timeline, leveraging 23 scRNA-seq and 3 scATAC-seq samples spanning wild-type, heterozygous, and knockout conditions.

## Key Findings

### 1. Developmental Cell Atlas
- Constructed a high-resolution cell type atlas across E10-P4 cortical development encompassing ~125,000 cells after quality control
- Identified distinct neural progenitor, intermediate progenitor, and neuronal populations with temporal resolution
- Cell type composition shifts dramatically between genotypes, particularly in deep-layer projection neurons

### 2. Critical Temporal Windows
- Fezf2 mutation phenotypes emerge around E13-E15, coinciding with peak corticofugal neuron specification
- Time-resolved differential expression reveals progressive transcriptional divergence between WT and KO
- Trajectory analysis (PAGA, pseudotime) shows aberrant cell fate decisions in KO, with progenitors failing to properly commit to corticofugal identity

### 3. Gene Dosage Effects
- **7,248 genes** show linear dose-response to Fezf2 dosage (WT > Het > KO)
- **13,782 genes** show no significant dose-dependent response
- Heterozygous mice activate partial compensatory programs, resulting in intermediate phenotypes
- Cell-type-specific buffering capacities vary, with committed projection neurons showing the least compensation

### 4. Sex-Specific Responses
- Male and female Fezf2 heterozygous mice at P1 show sexually dimorphic transcriptional profiles
- Sex-specific compensatory mechanisms identified, with implications for understanding sex bias in neurodevelopmental disorders

### 5. Gene Regulatory Networks
- Multi-omics integration (scRNA-seq + scATAC-seq) reveals Fezf2's role as a master regulator of corticofugal neuron specification
- Peak-to-gene linkage maps identify direct regulatory targets through chromatin accessibility changes
- Network perturbation analysis highlights key downstream effectors and feedback loops

### 6. Therapeutic Target Discovery
- Druggable gene categories identified among Fezf2-responsive genes (kinases, GPCRs, epigenetic modifiers)
- Therapeutic intervention window defined at E13-E15 for maximal efficacy
- Prioritized target list with mechanistic rationale for potential pharmacological rescue

## Dataset

**Source**: [GEO GSE153164](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153164) (Di Bella et al. 2021, Nature)

| Data Type | Samples | Conditions |
|-----------|---------|------------|
| scRNA-seq | 23 | WT time course (E10-P4), Het (E13, E15, P1 F/M), KO (E13, E15, P1) |
| scATAC-seq | 3 | WT (E13.5, E15.5, E18.5) |

**QC Summary**: 125,498 cells retained (97.5%) across 21,032 genes from 20 samples. Median 2,173 genes/cell, 5,298 UMI/cell, 4.14% mitochondrial reads.

## Analysis Workflow

The analysis is implemented in six sequential phases, all in Jupyter notebooks using the Python scverse ecosystem.

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5 ──► Phase 6
Preprocess   Temporal    Dose-       Multi-omics  Therapeutic  Validation
& Integrate  Analysis    Response    & GRN        Targets      & Figures
```

### Phase 1: Data Integration & Preprocessing
**Notebook**: `notebooks/01_preprocessing.ipynb`
- Quality control with MAD-based filtering (genes, UMI counts, mitochondrial %)
- Deep learning-based doublet detection
- Batch correction and integration using Harmony and scVI
- Dimensionality reduction (PCA, UMAP) and unsupervised clustering
- **Output**: Integrated AnnData object (~125k cells × 21k genes)

### Phase 2: Temporal & Developmental Analysis
**Notebook**: `notebooks/02_temporal_analysis.ipynb`
- High-resolution cell type annotation with marker gene scoring
- RNA velocity analysis (scVelo) for transcriptional dynamics
- Trajectory inference using PAGA and diffusion pseudotime
- Time-resolved differential expression (WT vs Het vs KO)
- Critical temporal window identification
- **Output**: 16 figures — cell type atlas, trajectories, velocity streams, pseudotime maps

### Phase 3: Dose-Response & Comparative Analysis
**Notebook**: `notebooks/03_dose_response.ipynb`
- Gene dosage effect modeling across WT → Het → KO
- Classification of genes by dose-response pattern (linear, threshold, compensatory)
- Sex-specific analysis (P1 Het Female vs Male)
- Cell type compositional analysis across conditions
- Cell entropy and aberrant state detection
- **Output**: 9 figures, gene classification lists (7,248 linear; 13,782 no-response)

### Phase 4: Multi-Omics Integration & GRN Analysis
**Notebook**: `notebooks/04_multiomics_grn.ipynb`
- Integration of scRNA-seq + scATAC-seq at matched timepoints (E13, E15, E18)
- Peak-to-gene linkage and enhancer-promoter mapping
- TF motif enrichment and chromatin accessibility analysis
- Gene regulatory network reconstruction
- Fezf2 direct target identification
- **Output**: Integrated multi-omics objects, GRN, direct target list

### Phase 5: Therapeutic Target Discovery
**Notebook**: `notebooks/05_therapeutic_targets.ipynb`
- Druggable gene identification (GPCRs, kinases, ion channels, epigenetic modifiers)
- Drug-gene interaction database queries (DGIdb, ChEMBL)
- Pathway-based target prioritization
- In silico perturbation predictions
- Therapeutic window determination
- **Output**: Ranked therapeutic target list, intervention window recommendations

### Phase 6: Validation & Manuscript Preparation
**Notebook**: `notebooks/06_validation.ipynb`
- Cross-validation with published datasets
- Publication-quality figure generation (PDF, TrueType fonts)
- Statistical validation frameworks
- Manuscript materials preparation
- **Output**: 56 publication-ready figures across all phases

## Project Structure

```
fezf2-multiomics/
├── notebooks/                  # Analysis notebooks (Phases 1-6)
│   ├── 01_preprocessing.ipynb
│   ├── 02_temporal_analysis.ipynb
│   ├── 03_dose_response.ipynb
│   ├── 04_multiomics_grn.ipynb
│   ├── 05_therapeutic_targets.ipynb
│   └── 06_validation.ipynb
├── data/
│   ├── raw/                    # Raw count matrices from GEO
│   ├── processed/              # Integrated AnnData objects
│   └── external/               # External reference data
├── results/
│   ├── preprocessing/          # QC and integration figures
│   ├── temporal/               # Cell type atlas, trajectories, velocity
│   ├── dose_response/          # Dose-response figures and gene lists
│   ├── multiomics/             # ATAC-seq integration outputs
│   ├── therapeutic/            # Drug target prioritization
│   └── qc/                     # QC summary metrics
├── docs/
│   ├── setup.md                # Environment setup guide
│   └── internal/               # Performance fixes documentation
├── RESEARCH_PLAN.md            # Detailed research plan and hypotheses
└── README.md
```

## Getting Started

### Prerequisites

- Python ≥ 3.11
- RAM: ≥ 128 GB recommended (integrated object is ~4.67 GB)
- Storage: ~500 GB for data and intermediate files

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd fezf2-multiomics

# Create conda environment
conda create -n fezf2 python=3.11
conda activate fezf2

# Install core dependencies
pip install scanpy anndata muon scvelo cellrank decoupler
pip install harmonypy scvi-tools
pip install matplotlib seaborn scipy statsmodels scikit-learn
pip install jupyter
```

### Running the Analysis

Execute notebooks sequentially:

```bash
jupyter lab notebooks/
```

1. Start with `01_preprocessing.ipynb` — downloads and processes raw data from GEO
2. Each subsequent notebook depends on outputs from previous phases
3. Results are saved to `results/` subdirectories

## Tools & Methods

| Category | Tools |
|----------|-------|
| Core framework | Scanpy, AnnData, Muon |
| Integration | Harmony, scVI |
| Velocity | scVelo |
| Trajectories | PAGA, Diffusion Pseudotime, CellRank |
| GRN | Decoupler, SCENIC |
| Multi-omics | Muon (RNA + ATAC) |
| Statistics | Scipy, Statsmodels, Scikit-learn |
| Visualization | Matplotlib, Seaborn |

## References

- Di Bella DJ, et al. (2021) Molecular logic of cellular diversification in the mouse cerebral cortex. *Nature* 595:554-559.
- Hao Y, et al. (2021) Integrated analysis of multimodal single-cell data. *Cell* 184:3573-3587.
- Bergen V, et al. (2020) Generalizing RNA velocity to transient cell states. *Nature Biotechnology* 38:1408-1414.
- Aibar S, et al. (2017) SCENIC: single-cell regulatory network inference and clustering. *Nature Methods* 14:1083-1086.

## License

This project is intended for academic research purposes.

## Acknowledgments

- Di Bella et al. for generating and sharing the GSE153164 dataset
- The scverse community and developers of Scanpy, scVelo, CellRank, and other tools used in this analysis
