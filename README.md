# Fezf2-Mediated Cortical Development: Multi-Omics Analysis

## Project Overview

This project presents a comprehensive multi-omics analysis of Fezf2-mediated cortical development, leveraging the GSE153164 dataset (Di Bella et al. 2021) to investigate temporal and cell-type-specific mechanisms by which Fezf2 mutations disrupt cortical development.

### Key Innovations

1. **Full developmental time course analysis** (E10-P4) across 23 scRNA-seq samples
2. **Gene dosage effects** using wild-type, heterozygous, and knockout samples
3. **Multi-omics integration** of scRNA-seq and scATAC-seq data
4. **Developmental trajectory reconstruction** and cell fate analysis
5. **Therapeutic target identification** through network-based approaches

## Research Goals

1. Identify critical temporal windows when Fezf2 mutation phenotypes emerge
2. Characterize developmental trajectory perturbations and aberrant cell fate decisions
3. Discover compensatory mechanisms in heterozygous conditions
4. Reconstruct gene regulatory networks and identify direct Fezf2 targets
5. Identify druggable therapeutic targets and optimal intervention windows

## Dataset Information

**Source**: GEO accession GSE153164 (Di Bella et al. 2021)

### scRNA-seq Samples (n=23)
- **Wild-type time course**: E10, E11.5, E12.5, E13.5, E14.5, E15.5, E16, E17.5, E18.5, P1 (2 replicates), P4
- **Fezf2 heterozygous**: E13, E15, P1 (Female), P1 (Male)
- **Fezf2 knockout**: E13, E15, P1

### scATAC-seq Samples (n=3)
- Wild-type: E13.5, E15.5, E18.5

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed directory organization.

```
nsr_acc/
├── data/                    # Raw and processed data
├── analysis/                # Analysis scripts (6 phases)
├── results/                 # Figures, tables, outputs
├── utils/                   # Utility functions
├── docs/                    # Documentation
├── config/                  # Configuration files
└── logs/                    # Analysis logs
```

## Analysis Pipeline

### Phase 1: Data Integration & Preprocessing (Weeks 1-3)
- Load all scRNA-seq and scATAC-seq samples
- Quality control and filtering
- Batch correction and integration
- Create multi-modal objects

**Tools**: Seurat v5, Harmony, scVI, Signac, ArchR

### Phase 2: Temporal & Developmental Analysis (Weeks 4-6)
- Cell type annotation across all timepoints
- RNA velocity analysis
- Trajectory inference
- Pseudotime ordering
- Time-resolved differential expression

**Tools**: scVelo, Monocle3, PAGA, Slingshot, CellRank

### Phase 3: Dose-Response & Comparative Analysis (Weeks 7-9)
- WT vs Het vs KO comparisons
- Dose-response modeling
- Sex-specific analysis (P1 Het Female vs Male)
- Cell type proportion analysis
- Compensatory mechanism identification

**Tools**: DESeq2, edgeR, limma, scCODA

### Phase 4: Multi-Omics Integration & GRN Analysis (Weeks 10-14)
- Integrate scRNA-seq + scATAC-seq
- Peak-to-gene linkage
- TF motif enrichment and footprinting
- Gene regulatory network reconstruction
- Direct target identification

**Tools**: Signac, ArchR, Cicero, chromVAR, SCENIC, CellOracle, MOFA+

### Phase 5: Therapeutic Target Discovery (Weeks 15-17)
- Druggable gene identification
- Drug-gene interaction database queries
- Pathway-based target prioritization
- In silico perturbation predictions
- Therapeutic window determination

**Tools**: DGIdb, ChEMBL, DrugBank, clusterProfiler, ReactomePA

### Phase 6: Validation & Manuscript Preparation (Weeks 18-20)
- Cross-validation with published datasets
- Publication-quality figure generation
- Statistical validation
- Manuscript writing

## Getting Started

### Prerequisites

**Software Requirements**:
- R (≥4.3.0)
- Python (≥3.9)
- RStudio (recommended)
- Jupyter Lab/Notebook

**Hardware Recommendations**:
- CPU: ≥16 cores (32+ ideal)
- RAM: ≥128 GB (256 GB ideal)
- Storage: ~500 GB
- GPU: Optional (beneficial for deep learning models)

### Installation

1. **Clone or download this repository**

2. **Set up R environment**:
   ```R
   # Install renv for dependency management
   install.packages("renv")

   # Restore R package environment
   renv::restore()

   # Or source the environment setup
   source("config/r_environment.R")
   ```

3. **Set up Python environment**:
   ```bash
   # Create conda environment
   conda env create -f config/python_environment.yml

   # Activate environment
   conda activate fezf2_analysis

   # Or use pip
   pip install -r requirements.txt
   ```

4. **Download data from GEO**:
   ```R
   # Run data download script
   source("analysis/phase1_data_integration/scripts/01_download_data.R")
   ```

## Expected Outcomes

### Scientific Contributions
1. First comprehensive multi-omics developmental atlas of Fezf2 mutation effects
2. Discovery of critical therapeutic windows for intervention
3. Identification of dose-dependent compensatory mechanisms
4. Prioritized list of druggable therapeutic targets
5. Direct Fezf2 target genes identified through multi-omics integration
6. Trajectory-based understanding of aberrant cell fate decisions
7. Sex-specific responses to Fezf2 haploinsufficiency

### Publications
**Target Journals**: Nature Neuroscience, Neuron, Cell, Nature Communications

**Manuscript Structure**:
- 8 main figures
- 10-15 extended data figures
- 6-7 supplementary tables
- Complete methods and code repository

## Key Research Questions

1. **RQ1.1**: When do Fezf2 mutation phenotypes first emerge during cortical development?
2. **RQ1.2**: How do developmental trajectories diverge between WT, Het, and KO conditions?
3. **RQ2.1**: Does Fezf2 haploinsufficiency trigger compensatory transcriptional responses?
4. **RQ2.2**: Are there sex-specific responses to Fezf2 haploinsufficiency?
5. **RQ3.1**: How does Fezf2 deficiency reshape gene regulatory networks?
6. **RQ3.2**: What are the direct transcriptional targets of Fezf2?
7. **RQ4.1**: Which cell types are most vulnerable to Fezf2 deficiency?
8. **RQ4.2**: Are there rare or transitional cell populations in mutant conditions?
9. **RQ5.1**: Can we identify druggable targets that rescue Fezf2 deficiency phenotypes?
10. **RQ5.2**: Can we predict critical intervention windows for maximal therapeutic efficacy?

## Data Availability

Upon publication, all processed data, analysis code, and interactive visualizations will be made publicly available:

- **Code**: GitHub repository (fully documented)
- **Processed Data**: Zenodo/Figshare
- **Interactive Browser**: Shiny app or cellxgene
- **Docker Container**: Reproducible analysis environment

## Contact

For questions about this analysis, please open an issue in the GitHub repository.

## References

**Primary Dataset**:
- Di Bella DJ, et al. (2021) Molecular logic of cellular diversification in the mouse cerebral cortex. Nature 595:554-559.

**Key Methodological References**:
- Hao Y, et al. (2021) Integrated analysis of multimodal single-cell data. Cell 184:3573-3587.
- Bergen V, et al. (2020) Generalizing RNA velocity to transient cell states. Nat Biotechnol 38:1408-1414.
- Aibar S, et al. (2017) SCENIC: single-cell regulatory network inference and clustering. Nat Methods 14:1083-1086.

See [research_plan.md](research_plan.md) for complete references and detailed methodology.

## License

This project is intended for academic research purposes.

## Acknowledgments

- Di Bella et al. for generating and sharing the GSE153164 dataset
- The developers of Seurat, Scanpy, SCENIC, and other computational tools used in this analysis

---

**Project Status**: Structure created, ready for Phase 1 implementation

**Last Updated**: 2025-10-25
