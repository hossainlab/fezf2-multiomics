import marimo

__generated_with = "0.17.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Phase 1: Data Integration & Preprocessing
    ## Fezf2 Multi-Omics Analysis - scRNA-seq Data

    **Goal**: Load all 23 scRNA-seq samples, perform comprehensive QC, and integrate data using scverse ecosystem

    **Dataset**: GSE153164 - Di Bella et al. 2021
    - Wild-type developmental time course: E10, E11.5, E12.5, E13.5, E14.5, E15.5, E16, E17.5, E18.5, P1 (2 replicates), P4
    - Fezf2 heterozygous: E13, E15, P1 (Female), P1 (Male)
    - Fezf2 knockout: E13, E15, P1

    **Tools**: scanpy, anndata, muon, scvi-tools, harmonypy
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Environment Setup & Import Libraries
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _():
    # Core libraries
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    import warnings
    warnings.filterwarnings('ignore')
    return Path, np, pd, plt


@app.cell
def _():
    # Scverse ecosystem
    import scanpy as sc
    import anndata as ad
    import muon as mu
    return ad, mu, sc


@app.cell
def _():
    # Integration tools
    try:
        import scvi
        print(f"scvi-tools version: {scvi.__version__}")
    except ImportError:
        print("scvi-tools not installed. Will use Harmony for integration.")

    try:
        import harmonypy
        print(f"harmonypy version: {harmonypy.__version__}")
    except ImportError:
        print("harmonypy not installed.")
    return


@app.cell
def _(ad, mu, sc):
    # Print versions
    print(f"scanpy version: {sc.__version__}")
    print(f"anndata version: {ad.__version__}")
    print(f"muon version: {mu.__version__}")
    return


@app.cell
def _(Path, sc):
    # Set plotting parameters
    sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
    sc.settings.set_figure_params(dpi=100, facecolor='white', frameon=False)
    sc.settings.figdir = Path('../results/phase1_preprocessing/figures')
    sc.settings.n_jobs = -1  # Use all available cores for parallel processing
    return


@app.cell
def _(np):
    # Random seed for reproducibility
    np.random.seed(42)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Define Sample Metadata

    We'll create a comprehensive metadata table for all 23 scRNA-seq samples.
    """)
    return


@app.cell
def _(pd):
    # Define sample metadata
    sample_metadata = pd.DataFrame([
        # Wild-type time course
        {'gsm_id': 'GSM5277843', 'filename': 'GSM5277843_E10_v1_filtered_feature_bc_matrix.h5', 
         'timepoint': 'E10', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch2'},
        {'gsm_id': 'GSM4635072', 'filename': 'GSM4635072_E11_5_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E11.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635073', 'filename': 'GSM4635073_E12_5_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E12.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635074', 'filename': 'GSM4635074_E13_5_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E13.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635075', 'filename': 'GSM4635075_E14_5_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E14.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635076', 'filename': 'GSM4635076_E15_5_S1_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E15.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635077', 'filename': 'GSM4635077_E16_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E16', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM5277844', 'filename': 'GSM5277844_E17_5_filtered_feature_bc_matrix.h5', 
         'timepoint': 'E17.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch2'},
        {'gsm_id': 'GSM4635078', 'filename': 'GSM4635078_E18_5_S1_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E18.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635079', 'filename': 'GSM4635079_E18_S3_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'E18.5', 'genotype': 'WT', 'sex': 'NA', 'replicate': 2, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635080', 'filename': 'GSM4635080_P1_S1_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'P1', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635081', 'filename': 'GSM4635081_P1_S2_filtered_gene_bc_matrices_h5.h5', 
         'timepoint': 'P1', 'genotype': 'WT', 'sex': 'NA', 'replicate': 2, 'batch': 'batch1'},
        {'gsm_id': 'GSM5277845', 'filename': 'GSM5277845_P4_filtered_feature_bc_matrix.h5', 
         'timepoint': 'P4', 'genotype': 'WT', 'sex': 'NA', 'replicate': 1, 'batch': 'batch2'},
    
        # Fezf2 heterozygous samples
        {'gsm_id': 'GSM4635088', 'filename': 'GSM4635088_Fezf2het_E13_filtered_feature_bc_matrix.h5', 
         'timepoint': 'E13', 'genotype': 'Het', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635082', 'filename': 'GSM4635082_Fezf2Het_E15_filtered_feature_bc_matrix.h5', 
         'timepoint': 'E15', 'genotype': 'Het', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635083', 'filename': 'GSM4635083_Fezf2Het_P1F_filtered_feature_bc_matrix.h5', 
         'timepoint': 'P1', 'genotype': 'Het', 'sex': 'Female', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635084', 'filename': 'GSM4635084_Fezf2Het_P1M_filtered_feature_bc_matrix.h5', 
         'timepoint': 'P1', 'genotype': 'Het', 'sex': 'Male', 'replicate': 1, 'batch': 'batch1'},
    
        # Fezf2 knockout samples
        {'gsm_id': 'GSM4635085', 'filename': 'GSM4635085_Fezf2KO_E13_filtered_feature_bc_matrix.h5', 
         'timepoint': 'E13', 'genotype': 'KO', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635086', 'filename': 'GSM4635086_Fezf2KO_E15_filtered_feature_bc_matrix.h5', 
         'timepoint': 'E15', 'genotype': 'KO', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
        {'gsm_id': 'GSM4635087', 'filename': 'GSM4635087_Fezf2KO_P1_filtered_feature_bc_matrix.h5', 
         'timepoint': 'P1', 'genotype': 'KO', 'sex': 'NA', 'replicate': 1, 'batch': 'batch1'},
    ])

    # Create sample_id combining timepoint and genotype
    sample_metadata['sample_id'] = sample_metadata.apply(
        lambda x: f"{x['timepoint']}_{x['genotype']}" + (f"_{x['sex']}" if x['sex'] != 'NA' else '') + 
                  (f"_rep{x['replicate']}" if x['replicate'] > 1 or (x['timepoint'] == 'P1' and x['genotype'] == 'WT') else ''),
        axis=1
    )
    sample_metadata
    return (sample_metadata,)


@app.cell
def _(sample_metadata):
    len(sample_metadata)
    return


@app.cell
def _(sample_metadata):
    sample_metadata['genotype'].value_counts()
    return


@app.cell
def _(sample_metadata):
    sample_metadata['timepoint'].value_counts().sort_index()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Load Single Sample for Initial Exploration

    Let's start by loading one sample to understand the data structure and set QC parameters.
    """)
    return


@app.cell
def _(Path, sc):
    # Load one sample for exploration (E13.5 WT)
    data_dir = Path('../data/scRNA-seq')
    test_file = data_dir / 'GSM4635074_E13_5_filtered_gene_bc_matrices_h5.h5'

    print(f"Loading test sample: {test_file.name}")
    adata_test = sc.read_10x_h5(test_file, gex_only=True)

    print(f"\nShape: {adata_test.shape[0]} cells × {adata_test.shape[1]} genes")
    print(f"\nFirst 5 genes: {adata_test.var_names[:5].tolist()}")
    print(f"\nVariable names (columns in .var):")
    print(adata_test.var.head())
    return (data_dir,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Load All Samples

    Now we'll load all 23 scRNA-seq samples and add metadata to each.
    """)
    return


@app.cell
def _(data_dir, sample_metadata, sc):
    # Function to load and annotate a single sample
    def load_sample(row, data_dir):
        """
        Load a single 10x h5 file and add metadata.
        """
        filepath = data_dir / row['filename']
        print(f"Loading {row['sample_id']}... ", end='')
    
        try:
            # Read 10x h5 file
            adata = sc.read_10x_h5(filepath, gex_only=True)
        
            # Make variable names unique
            adata.var_names_make_unique()
        
            # Add metadata to obs (cell-level)
            adata.obs['sample_id'] = row['sample_id']
            adata.obs['gsm_id'] = row['gsm_id']
            adata.obs['timepoint'] = row['timepoint']
            adata.obs['genotype'] = row['genotype']
            adata.obs['sex'] = row['sex']
            adata.obs['replicate'] = row['replicate']
            adata.obs['batch'] = row['batch']
        
            print(f"{adata.shape[0]} cells")
            return adata
        
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return None

    # Load all samples
    print("Loading all 20 scRNA-seq samples...\n")
    adatas = []

    for idx, row in sample_metadata.iterrows():
        adata = load_sample(row, data_dir)
        if adata is not None:
            adatas.append(adata)

    print(f"\nSuccessfully loaded {len(adatas)} samples")
    return (adatas,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Concatenate All Samples

    Merge all samples into a single AnnData object for integrated analysis.
    """)
    return


@app.cell
def _(ad, adatas):
    # Concatenate all samples
    print("Concatenating all samples...")
    adata_all = ad.concat(
        adatas,
        join='outer',  # Keep all genes (union)
        merge='unique',  # Make cell barcodes unique
        label='sample_id',
        keys=[adata.obs['sample_id'].iloc[0] for adata in adatas],
        index_unique='_'
    )

    print(f"\nCombined dataset: {adata_all.shape[0]:,} cells × {adata_all.shape[1]:,} genes")
    print(f"\nMemory usage: {adata_all.X.data.nbytes / 1e9:.2f} GB")

    # Display summary
    print("\nCells per sample:")
    print(adata_all.obs['sample_id'].value_counts())
    return (adata_all,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Step 6: Calculate QC Metrics

    Calculate quality control metrics:
    - Number of genes per cell
    - Total UMI counts per cell
    - Mitochondrial gene percentage
    - Ribosomal gene percentage
    """)
    return


@app.cell
def _(adata_all, sc):
    # Identify mitochondrial genes (genes starting with 'mt-' or 'Mt-')
    adata_all.var['mt'] = adata_all.var_names.str.startswith(('mt-', 'Mt-'))
    print(f"Mitochondrial genes found: {adata_all.var['mt'].sum()}")

    # Identify ribosomal genes (genes starting with 'Rpl' or 'Rps')
    adata_all.var['ribo'] = adata_all.var_names.str.match('^Rp[sl]')
    print(f"Ribosomal genes found: {adata_all.var['ribo'].sum()}")

    # Calculate QC metrics
    print("\nCalculating QC metrics...")
    sc.pp.calculate_qc_metrics(
        adata_all,
        qc_vars=['mt', 'ribo'],
        percent_top=None,
        log1p=False,
        inplace=True
    )

    print("\nQC metrics added to .obs:")
    print(adata_all.obs.columns.tolist())
    return


@app.cell
def _(adata_all):
    # Display QC statistics
    qc_metrics = adata_all.obs[[
        'n_genes_by_counts',
        'total_counts',
        'pct_counts_mt',
        'pct_counts_ribo'
    ]]

    qc_metrics
    return (qc_metrics,)


@app.cell
def _(qc_metrics):
    qc_metrics.describe()
    return


@app.cell
def _(adata_all, plt, sc):
    # QC violin plots by sample
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Number of genes
    sc.pl.violin(adata_all, 'n_genes_by_counts', groupby='sample_id',
                 rotation=90, ax=axes[0,0], show=False)
    axes[0,0].set_title('Number of Genes per Cell')
    axes[0,0].text(-0.1, 1.05, 'A', transform=axes[0,0].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Total counts
    sc.pl.violin(adata_all, 'total_counts', groupby='sample_id',
                 rotation=90, ax=axes[0,1], show=False)
    axes[0,1].set_title('Total UMI Counts per Cell')
    axes[0,1].text(-0.1, 1.05, 'B', transform=axes[0,1].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Mitochondrial percentage
    sc.pl.violin(adata_all, 'pct_counts_mt', groupby='sample_id',
                 rotation=90, ax=axes[1,0], show=False)
    axes[1,0].set_title('Mitochondrial Gene %')
    axes[1,0].axhline(y=20, color='red', linestyle='--', label='20% threshold')
    axes[1,0].legend()
    axes[1,0].text(-0.1, 1.05, 'C', transform=axes[1,0].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Ribosomal percentage
    sc.pl.violin(adata_all, 'pct_counts_ribo', groupby='sample_id',
                 rotation=90, ax=axes[1,1], show=False)
    axes[1,1].set_title('Ribosomal Gene %')
    axes[1,1].text(-0.1, 1.05, 'D', transform=axes[1,1].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig('../results/phase1_preprocessing/figures/01_qc_violin_by_sample.pdf', bbox_inches='tight')
    plt.show()
    return


@app.cell
def _(adata_all, plt):
    # Overall QC distributions
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # Genes per cell histogram
    axes[0,0].hist(adata_all.obs['n_genes_by_counts'], bins=100, edgecolor='black')
    axes[0,0].set_xlabel('Number of genes')
    axes[0,0].set_ylabel('Number of cells')
    axes[0,0].set_title('Genes per Cell Distribution')
    axes[0,0].axvline(x=200, color='red', linestyle='--', label='Min threshold (200)')
    axes[0,0].axvline(x=6000, color='orange', linestyle='--', label='Max threshold (6000)')
    axes[0,0].legend()
    axes[0,0].text(-0.15, 1.05, 'A', transform=axes[0,0].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # UMI counts histogram
    axes[0,1].hist(adata_all.obs['total_counts'], bins=100, edgecolor='black')
    axes[0,1].set_xlabel('Total UMI counts')
    axes[0,1].set_ylabel('Number of cells')
    axes[0,1].set_title('UMI Counts per Cell Distribution')
    axes[0,1].set_xlim(0, 20000)
    axes[0,1].text(-0.15, 1.05, 'B', transform=axes[0,1].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Mitochondrial % histogram
    axes[0,2].hist(adata_all.obs['pct_counts_mt'], bins=100, edgecolor='black')
    axes[0,2].set_xlabel('Mitochondrial %')
    axes[0,2].set_ylabel('Number of cells')
    axes[0,2].set_title('Mitochondrial Gene % Distribution')
    axes[0,2].axvline(x=20, color='red', linestyle='--', label='Max threshold (20%)')
    axes[0,2].legend()
    axes[0,2].text(-0.15, 1.05, 'C', transform=axes[0,2].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Scatter: UMI vs Genes
    axes[1,0].scatter(adata_all.obs['total_counts'], adata_all.obs['n_genes_by_counts'],
                      s=1, alpha=0.3, rasterized=True)
    axes[1,0].set_xlabel('Total UMI counts')
    axes[1,0].set_ylabel('Number of genes')
    axes[1,0].set_title('UMI vs Genes Detected')
    axes[1,0].set_xlim(0, 20000)
    axes[1,0].text(-0.15, 1.05, 'D', transform=axes[1,0].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Scatter: UMI vs MT%
    axes[1,1].scatter(adata_all.obs['total_counts'], adata_all.obs['pct_counts_mt'],
                      s=1, alpha=0.3, rasterized=True)
    axes[1,1].set_xlabel('Total UMI counts')
    axes[1,1].set_ylabel('Mitochondrial %')
    axes[1,1].set_title('UMI vs Mitochondrial %')
    axes[1,1].axhline(y=20, color='red', linestyle='--')
    axes[1,1].set_xlim(0, 20000)
    axes[1,1].text(-0.15, 1.05, 'E', transform=axes[1,1].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    # Scatter: Genes vs MT%
    axes[1,2].scatter(adata_all.obs['n_genes_by_counts'], adata_all.obs['pct_counts_mt'],
                      s=1, alpha=0.3, rasterized=True)
    axes[1,2].set_xlabel('Number of genes')
    axes[1,2].set_ylabel('Mitochondrial %')
    axes[1,2].set_title('Genes vs Mitochondrial %')
    axes[1,2].axhline(y=20, color='red', linestyle='--')
    axes[1,2].text(-0.15, 1.05, 'F', transform=axes[1,2].transAxes,
                   fontsize=16, fontweight='bold', va='top')

    plt.tight_layout()
    plt.savefig('../results/phase1_preprocessing/figures/02_qc_distributions.pdf', bbox_inches='tight')
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
