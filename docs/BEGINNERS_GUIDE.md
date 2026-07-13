# A Beginner's Guide to the Fezf2 Multi-Omics Project

**Who this is for:** someone with zero background in genomics or single-cell biology who needs to understand what this project does, why each step exists, and what the results mean.

You do not need to know any biology to start. Every term is defined the first time it appears, and every technical step is paired with an everyday analogy.

---

## Part 1 — The Biology, From Scratch

### 1.1 Genes, and why cells differ

Every cell in a mouse carries the **same** DNA — the same ~20,000 genes. A neuron and a skin cell are genetically identical. So why are they different?

Because they **use** different genes.

> **Analogy — the cookbook.** DNA is a cookbook with 20,000 recipes. Every kitchen in the country has an identical copy. But the pizzeria only ever cooks from the pizza recipes, and the bakery only cooks from the bread recipes. Same book, different pages in use. That is what makes a pizzeria a pizzeria.

When a cell "cooks from" a gene, we say the gene is **expressed**. The cell makes a working copy of that recipe, called **mRNA** (messenger RNA), and hands it to the machinery that builds proteins. The set of all mRNA in a cell is its **transcriptome** — a snapshot of exactly which recipes that cell is cooking right now.

**Measuring the transcriptome is the entire foundation of this project.** If you can read which genes a cell is expressing, you can infer what kind of cell it is and what it is doing.

### 1.2 Transcription factors: the genes that control other genes

Most genes encode "worker" proteins — structural parts, enzymes, and so on. But a special class of genes encodes **transcription factors** (TFs): proteins whose job is to switch *other* genes on and off.

> **Analogy — the head chef.** Most recipes produce a dish. But a transcription factor is not a dish — it is the head chef who walks into the kitchen and says *"tonight we're doing Italian."* One decision, and dozens of downstream recipes get pulled off the shelf while others get put away. TFs are **master switches**.

This matters enormously: mutate one worker gene and you lose one protein. Mutate one *transcription factor* and you can derail an entire developmental program, because everything downstream of it changes at once.

### 1.3 Fezf2 — the gene this project is about

**Fezf2** is a transcription factor active in the developing mouse **cerebral cortex** (the wrinkled outer layer of the brain that handles perception, movement, and thought).

The cortex is built in **layers**, roughly like a six-layer cake, and each layer contains a different type of neuron with a different job. Crucially, the layers are built **from the inside out**, and the neurons are born on a schedule — deep layers first, upper layers later.

Fezf2's known role: it tells a young neuron *"you are going to be a deep-layer neuron that sends a long wire down to the spinal cord and brainstem."* These are called **subcerebral projection neurons** — the ones that carry motor commands out of the brain. Without Fezf2, those neurons fail to acquire that identity.

> **Analogy — the career counselor.** Imagine a school where every graduate must pick a career. Fezf2 is the counselor who steers certain students toward "long-haul truck driver" (a neuron that projects a long axon to the spinal cord). Remove the counselor, and those students still graduate — but they drift into some *other* career instead. The school still produces people; it just produces the wrong mix.

### 1.4 The experiment: dosage

Genes come in **two copies** (one from each parent). This project studies three **genotypes** — three different "doses" of working Fezf2:

| Genotype | Working copies of Fezf2 | Nickname |
|---|---|---|
| **WT** (wild-type) | 2 | Normal |
| **Het** (heterozygous) | 1 | Half dose |
| **KO** (knockout) | 0 | No dose |

The central question is: **as you dial Fezf2 from 2 → 1 → 0, how does the developing brain respond?**

This is a *dose-response* question, and it is far more informative than a simple on/off comparison. Consider what different answers would mean:

- If a gene's expression falls smoothly 2 → 1 → 0, it tracks Fezf2 dosage directly. (**Linear**)
- If a gene looks totally normal at 1 copy but breaks at 0 copies, the cell has a **buffer** — one copy is enough. (**Threshold**)
- If a gene goes *up* when Fezf2 goes down, the cell may be **fighting back**, trying to compensate for the loss. (**Compensatory** — and these are the most interesting, because a drug that boosts a natural compensation mechanism is a plausible therapy.)

> **Analogy — dimming the lights.** Turn a dimmer from 100% → 50% → 0%. Some things in the room dim proportionally (linear). Some things are fine at 50% and only fail in total darkness (threshold). And some things *turn on* as it gets dark — like a motion-sensor nightlight kicking in (compensatory). The nightlight is what you'd want to build a therapy around.

---

## Part 2 — The Measurement Technologies

### 2.1 Single-cell RNA sequencing (scRNA-seq)

Older methods ground up an entire piece of tissue and measured the average gene expression across all of it. This hides everything interesting.

> **Analogy — smoothie vs. fruit salad.** Blend a fruit bowl into a smoothie and measure it: you learn the average sugar content. You cannot tell whether you had 10 bananas, or 5 bananas and 5 apples. **Bulk RNA-seq is the smoothie.** **Single-cell RNA-seq is the fruit salad** — you measure every piece separately, so you can count exactly how many bananas and apples there were, and spot the one weird kiwi.

Mechanically, scRNA-seq isolates each cell into its own tiny droplet, tags all the mRNA in that droplet with a unique **barcode** (so you can tell later which cell it came from), and sequences everything at once.

The output is a giant table:

|             | Fezf2 | Bcl11b | Sox2 | … 20,000 genes |
|-------------|-------|--------|------|----------------|
| **Cell 1**  | 0     | 3      | 15   | …              |
| **Cell 2**  | 7     | 22     | 0    | …              |
| **Cell 3**  | 0     | 0      | 9    | …              |
| … 121,869 cells | … | …    | …    | …              |

Each number is a **count** — how many mRNA copies of that gene were found in that cell. Most entries are **zero**, because any given cell only expresses a fraction of the genome at any moment. This matters computationally (see §2.3).

### 2.2 Single-cell ATAC-seq (scATAC-seq)

scRNA-seq tells you which recipes are being *cooked*. scATAC-seq tells you which pages of the cookbook are *physically open*.

DNA is not a loose string — it is wound tightly around proteins, like thread on a spool. A gene that is spooled up tight cannot be read. For a gene to be usable, its region must be **open** (accessible). ATAC-seq measures exactly this: which stretches of DNA are open in each cell.

> **Analogy — the open book.** RNA-seq is a photo of the dishes coming out of the kitchen. ATAC-seq is a photo of the cookbook lying on the counter, showing which pages are open. A page can be open without a dish being made yet — so ATAC often reveals what a cell is *about to* do, or what it is *capable of* doing. It's the regulatory layer beneath expression.

The open regions are called **peaks**. This project has 3 scATAC-seq samples with ~152,000 peaks each.

**"Multi-omics"** simply means combining more than one of these measurement types — here, RNA (what's expressed) plus ATAC (what's accessible).

### 2.3 A crucial technical detail: sparse matrices

That expression table is 121,869 cells × 20,000 genes ≈ **2.4 billion numbers**, and roughly 90–95% of them are zero.

Storing all 2.4 billion would take ~20 GB of RAM and crash a laptop. Instead the data is stored **sparsely**: only the non-zero values are recorded, along with their positions.

> **Analogy — the mostly-empty stadium.** To record who attended a 100,000-seat stadium with 300 people in it, you don't write down 100,000 rows of "empty." You just list the 300 occupied seat numbers. That's a sparse matrix.

This is why `CLAUDE.md` in this repo insists you keep the matrix sparse and never accidentally "densify" it — several operations (notably the Wilcoxon statistical test) secretly expand the whole thing to its full 20 GB size and blow up the machine. It is the single most common way to crash this pipeline.

---

## Part 3 — The Dataset

The data comes from **GSE153164** (Di Bella et al., 2021, *Nature*), a public dataset on the GEO repository.

| | |
|---|---|
| **scRNA-seq samples** | 20 |
| **Cells (after quality filtering)** | 121,869 |
| **Timepoints** | E10 → P4 (13 stages) |
| **Genotypes** | WT, Het, KO |
| **scATAC-seq samples** | 3 (E13.5, E15.5, E18.5 — all WT) |
| **scATAC cells** | 31,663 |

**Reading the timepoints:** `E13` = *embryonic day 13* (13 days after conception; the mouse is still in the womb). `P1` = *postnatal day 1* (one day after birth). Mice are born around E19–E20. So the dataset follows the brain from early construction (E10) through birth and into early life (P4).

> **A limitation you must know up front.** WT, Het, and KO were **not** all sampled at every timepoint. At `E13` and `E15` there are only Het and KO animals — **no WT**. The wild-type animals were collected at `E13.5` and `E15.5` instead, which the pipeline treats as different timepoints. **`P1` is the only timepoint with all three genotypes present.** This single fact causes real problems downstream, and it is flagged again in Part 5.

---

## Part 4 — The Six Phases, Explained

The project is six Jupyter notebooks that **must be run in order**, because each one reads the file the previous one wrote.

> **Analogy — the assembly line.** Phase 1 washes and chops the vegetables. Phase 2 labels each one. Phase 3 compares them across conditions. You cannot label what you haven't chopped.

The shared file format is **`.h5ad`** (an "AnnData" object). Think of it as a spreadsheet with attachments:

- `adata.X` — the big expression matrix (cells × genes)
- `adata.obs` — one row of metadata **per cell** (its genotype, timepoint, sex, cell type…)
- `adata.var` — one row of metadata **per gene**
- `adata.obsm` — alternative "views" of the cells (e.g. UMAP coordinates)

---

### Phase 1 — `01_preprocessing.ipynb` — Cleaning the data

Raw single-cell data is noisy. This phase throws out the junk.

**Quality control (QC).** Some "cells" in the data aren't healthy cells at all:
- A droplet with **too few genes** detected is probably just ambient debris, not a real cell.
- A droplet with **too many genes** is probably *two* cells stuck together.
- A cell with a high fraction of **mitochondrial** genes is probably dying. (Mitochondria are the cell's power plants. When a cell ruptures, its normal mRNA leaks out but the mitochondrial mRNA — protected inside the mitochondria — stays behind. So a high mitochondrial percentage is the signature of a corpse.)

> **Analogy — quality control on the fruit salad.** Before counting your fruit, you throw out the mush at the bottom of the bowl (debris), the two apples that got stuck together (doublets), and anything visibly rotten (dying cells).

**Doublet detection.** A "doublet" is two cells that got captured in one droplet and now masquerade as a single weird hybrid cell. Left in, they invent fake "intermediate" cell types that don't exist. Tools (`Solo`, `Scrublet`) simulate artificial doublets and learn to spot the real ones.

**Batch correction — the most conceptually important step here.** Samples processed on different days differ for purely *technical* reasons (different reagent batches, different machine runs). If uncorrected, your cells cluster by *which day they were processed* rather than by *what type of cell they are* — a catastrophic confound.

> **Analogy — photos in different lighting.** You photograph 20 people, but some shots are in warm indoor light and some in cold daylight. Sort by raw pixel color and you'll group them by *lighting*, not by *person*. Batch correction is color-correcting all the photos to a common white balance so that you group by the thing you actually care about.

This project uses two methods, **Harmony** and **scVI**, and compares them. scVI is a neural network that learns a clean, compressed representation of each cell (stored in `adata.obsm['X_scVI']`) with the batch effect stripped out.

**Clustering (Leiden).** Finally, cells with similar expression profiles are grouped. The **Leiden** algorithm builds a network where each cell links to its nearest neighbors, then finds densely-connected communities.

> **Analogy — friendship groups.** Draw a line between every pair of people who are friends, then look for the tight-knit clusters. Those clusters are the social groups — nobody labeled them, they emerged from the connections.

Importantly, clustering is **unsupervised**: it gives you groups labeled `0, 1, 2, 3…`, with no idea what they *are*. Naming them is Phase 2's job.

**Output:** a cleaned, integrated, clustered dataset.

---

### Phase 2 — `02_temporal_analysis.ipynb` — Naming the cells and ordering them in time

**Cell type annotation.** Phase 1 gave us anonymous clusters. Now we identify them using **marker genes** — genes known to be expressed by one specific cell type.

> **Analogy — identifying professions by their tools.** You have 14 groups of people and no labels. But one group is all carrying stethoscopes → doctors. One group is carrying hammers → carpenters. Marker genes are the tools. If a cluster strongly expresses `Sox2` and `Pax6` (stem-cell markers), it's a progenitor. If it expresses `Bcl11b`, it's a deep-layer neuron.

This produced **14 cell types** across 121,869 cells:

| Cell type | Cells | What it is |
|---|---|---|
| Cycling Progenitors | 20,335 | Dividing stem cells |
| Layer 2/3 Neurons | 20,256 | Upper-layer neurons (born late) |
| Intermediate Progenitors | 18,275 | Stem cells one step from becoming neurons |
| Corticothalamic Neurons | 16,179 | Deep-layer, project to thalamus |
| Layer 4 Neurons | 13,261 | Receive sensory input |
| GABAergic Interneurons | 11,745 | Inhibitory ("brake") neurons |
| Radial Glia | 9,999 | The original neural stem cells |
| **Subcerebral Projection Neurons** | 4,812 | **The Fezf2-dependent ones** |
| …and 6 rarer types | | |

**Trajectory analysis (PAGA + diffusion pseudotime).** Development is a continuous process: a stem cell gradually becomes a neuron. But our data is a set of *frozen snapshots* — we killed the mice and measured. We never watched a single cell change.

The trick: with 121,869 cells, we captured cells at every stage of the journey simultaneously. So we can **reconstruct** the path by ordering cells along a continuum from "most stem-like" to "most mature." That ordering is called **pseudotime**.

> **Analogy — the crowded staircase.** You are given one photograph of a thousand people on a staircase. You never see anyone move. But you can still confidently reconstruct the route from bottom to top, because people are standing on every step. Pseudotime is inferring the journey from a single crowded snapshot.

**RNA velocity** goes further. It exploits a quirk: newly-made mRNA still contains **introns** (unedited filler segments that get spliced out shortly after). If a cell is full of *unspliced* (intron-containing) mRNA for a gene, that gene was switched on *very recently* — so the cell is heading toward a state where that gene matters.

> **Analogy — wet paint.** Walk into a room and see fresh wet paint on one wall. You didn't watch anyone paint, but you know which wall was painted *most recently* — and therefore which direction the work is moving. Unspliced mRNA is wet paint. It gives each cell an arrow pointing toward its future.

**Output:** `results/temporal/adata_annotated.h5ad` — the master file every later phase reads.

---

### Phase 3 — `03_dose_response.ipynb` — How genes react to losing Fezf2

This is where the core question gets answered.

**Pseudobulk.** Counterintuitively, we now *undo* some of the single-cell resolution. For each sample, we sum up all its cells into one combined profile.

> **Analogy — back to the smoothie, on purpose.** We separated the fruit so we could *count* the bananas. Now, to compare orchard A against orchard B fairly, we blend each orchard's fruit back into a smoothie. Comparing individual cells across animals is statistically treacherous (cells from one mouse aren't independent samples); comparing one summarized profile per animal is honest.

**Classification.** For each gene, we look at its expression across WT (2 copies) → Het (1) → KO (0), and assign a pattern. Results at P1:

| Pattern | Genes | Meaning |
|---|---|---|
| **No Response** | 1,320 | Doesn't care about Fezf2 |
| **Linear** | 724 | Tracks Fezf2 dosage smoothly |
| **Compensatory** | 694 | Goes **up** as Fezf2 goes **down** — the "nightlight" genes |
| **Threshold** | 248 | Fine with 1 copy, breaks at 0 |
| **Synergistic** | 14 | Effects amplify non-additively |

The 694 **compensatory** genes are the therapeutic prize: the brain is already trying to fix itself, and these genes are the attempt.

**Sex-specific analysis.** The P1 Het samples were split by sex, revealing **503 sex-dimorphic genes** (157 female-biased, 346 male-biased) — meaning male and female brains do not respond to Fezf2 loss identically. This is exactly the kind of effect that gets missed when sex is ignored.

---

### Phase 4 — `04_multiomics_grn.ipynb` — Building the regulatory network

A **gene regulatory network (GRN)** is a wiring diagram: which transcription factor controls which genes.

> **Analogy — the org chart.** You want to know who reports to whom in a company. You can't see the org chart directly, so you observe: every time the manager comes in early, these five people also come in early. That correlation *suggests* a reporting line.

This is exactly what the notebook does: it correlates each TF's expression against every other gene, across cells. Genes that move in lockstep with Fezf2 are candidate **targets**.

It also loads the **scATAC-seq** data here (31,663 cells) to check which DNA regions are physically open — evidence about *where* a TF could actually bind.

**Be honest about this result:** using a correlation threshold of r > 0.3, Fezf2 came out with only **2 correlated targets** (`Stmn1` and `Tubb2b`, both r ≈ 0.31). That is a very thin network. It reflects a real limitation, not a bug — Fezf2 is expressed in a minority of cells, and correlation across a mixed population is a blunt instrument. See Part 5.

> **The critical caveat: correlation is not causation.** Ice-cream sales correlate with drowning deaths — because both rise in summer, not because ice cream drowns people. A gene correlated with Fezf2 might be *regulated by* Fezf2, or might just be switched on by the same upstream signal. The network is a list of **hypotheses**, not proven wiring.

---

### Phase 5 — `05_therapeutic_targets.ipynb` — Can we drug any of this?

Take the 694 compensatory genes and ask: **is there already a drug for any of them?**

The notebook queries **DGIdb** (the Drug–Gene Interaction Database), a public catalogue of known drug-gene relationships.

> **Analogy — checking the pharmacy shelf.** You've identified 694 doors the brain is trying to open. Before designing a brand-new key from scratch (10+ years, ~$1B), you check whether any existing key already fits. Repurposing an approved drug is enormously faster than inventing one.

**Result: 179 drug-gene interactions across 14 genes and 166 distinct drugs.**

Top-ranked target: **`Erbb4`** (59 known drugs). Erbb4 is a receptor with genuine, well-documented roles in cortical interneuron development — a biologically sensible hit, not noise. Others include `Cxcr4` (60 drugs) and `Ptprc` (18 drugs).

Genes are scored on multiple criteria — is it compensatory, does it have drugs, is it in the Fezf2 network, how big is the effect — and a gradient-boosting model ranks them.

---

### Phase 6 — `06_validation.ipynb` — Making the figures

The final phase produces the publication-ready outputs: **6 main figures**, **5 supplementary tables**, and a methods template. Figures are saved as **PDF** (a vector format — infinitely zoomable, and editable in Illustrator, which journals require) rather than PNG.

---

## Part 5 — What to Be Skeptical About

A good scientist reads results critically. Here is what is genuinely weak in this project, stated plainly.

**1. The missing wild-type controls.** As noted in Part 3, `E13` and `E15` have **no WT cells at all**. The dose-response analysis at those timepoints therefore compares Het and KO against a wild-type mean of *zero* — which is meaningless. **Only the P1 results are a genuine three-genotype comparison.** (Phase 4 additionally compares E13.5 WT networks against E13 Het/KO networks — half a day apart — without flagging it.)

**2. The dose statistics rest on n=3.** The "Linear," "Compensatory," etc. labels come from a Spearman correlation across **three** points (the WT, Het, and KO means). With only 3 points, the p-value is nearly meaningless — a perfect monotonic trend automatically yields p ≈ 0. Treat these categories as **descriptive**, not as statistically-proven claims.

**3. The Fezf2 network is thin.** Two targets above threshold is not a network. Any claim about "the Fezf2 regulatory program" from this data should be heavily hedged.

**4. Human drugs for mouse genes.** DGIdb catalogues *human* genes. To query it, the pipeline upper-cases mouse gene symbols (`Erbb4` → `ERBB4`) to match the human ortholog by name. This is a standard shortcut, but it is an approximation — mouse and human orthologs do not always behave identically.

**5. Correlation ≠ causation** (see Phase 4). Nothing here proves Fezf2 *causes* any of these changes. That requires a wet-lab experiment.

**6. Some hardcoded numbers in the summary are stale.** `manuscript_statistics.json` says "23 scRNA-seq samples" and "20 TFs analyzed"; the actual figures are **20 samples** and **15 TFs**. Trust the data files over the summary text.

---

## Part 6 — Glossary

| Term | Plain meaning |
|---|---|
| **AnnData / `.h5ad`** | The file format holding the cells × genes matrix plus all metadata |
| **ATAC-seq** | Measures which DNA regions are physically open/accessible |
| **Batch effect** | Fake differences caused by processing samples on different days |
| **Cortex** | Outer layer of the brain; built in ~6 layers, inside-out |
| **Doublet** | Two cells wrongly captured as one; must be removed |
| **E13 / P1** | Embryonic day 13 / Postnatal day 1 |
| **Expression** | How actively a gene is being "cooked" into mRNA |
| **Fezf2** | The transcription factor this project studies |
| **GRN** | Gene regulatory network — the TF→target wiring diagram |
| **Het / KO / WT** | 1 / 0 / 2 working copies of Fezf2 |
| **HVG** | Highly variable genes — the ~3,000 most informative genes, used to cut noise and compute cost |
| **Leiden** | The clustering algorithm that finds groups of similar cells |
| **Marker gene** | A gene whose expression identifies a specific cell type |
| **Mitochondrial %** | High value = the cell was dying |
| **mRNA** | The working copy of a gene's recipe |
| **Peak** | An open, accessible stretch of DNA (from ATAC-seq) |
| **Pseudobulk** | Summing all cells in a sample back into one profile for fair statistics |
| **Pseudotime** | Inferred developmental progress, reconstructed from static snapshots |
| **RNA velocity** | Using unspliced mRNA ("wet paint") to infer each cell's future direction |
| **scRNA-seq** | Measures gene expression in each cell individually |
| **Sparse matrix** | Memory-efficient storage that records only the non-zero values |
| **Transcription factor** | A gene that controls other genes — a master switch |
| **UMAP** | A 2-D map that places similar cells near each other, for visualization |

---

## Part 7 — Running It Yourself

The environment is managed with **uv** (not conda — any conda instructions elsewhere in this repo are outdated).

```bash
uv sync                # install the exact environment from uv.lock
uv run jupyter lab     # launch Jupyter
```

Then run the notebooks **strictly in order**, `01` → `06`. Each reads what the last one wrote, so skipping one will fail.

**Where things land:**
- Data objects → `data/processed/` and `results/preprocessing/`, `results/temporal/`
- Figures and tables → `results/<phase>/`
- Final manuscript figures → `results/validation/manuscript_figures/`

**The one rule that will save you hours:** never run a Wilcoxon differential-expression test on the full dataset. It silently converts the sparse matrix to dense (~20 GB) and kills the machine. Use `method='t-test_overestim_var'` instead — it is 10–100× faster and stays under 4 GB.

---

## Part 8 — The One-Paragraph Summary

Fezf2 is a master-switch gene that tells young neurons in the mouse cortex to become long-range motor-output neurons. This project takes 121,869 individual brain cells from mice with 2, 1, or 0 working copies of Fezf2, sampled across 13 stages of development, and asks how the developing brain responds as that switch is dialed down. After cleaning the data and identifying 14 cell types, it finds that **694 genes go *up* as Fezf2 goes down** — the brain appears to be actively compensating. Cross-referencing those genes against a drug database turns up **179 existing drugs** hitting 14 of them, headed by `Erbb4`. The headline caveat: only the postnatal-day-1 timepoint has all three genotypes present, so that is the only place the dose-response comparison is fully trustworthy.
