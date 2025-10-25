import re, yaml, json
from pathlib import Path
import pandas as pd

def load_cfg(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def discover_samples(cfg):
    raw = Path(cfg["paths"]["raw"])
    rna_pat = re.compile(cfg["patterns"]["rna"])
    atac_pat = re.compile(cfg["patterns"]["atac"])
    rna_files = [str(p) for p in raw.iterdir() if rna_pat.match(p.name)]
    atac_files = [str(p) for p in raw.iterdir() if atac_pat.match(p.name)]
    return rna_files, atac_files

def parse_meta_from_names(files, regex, cond_map):
    rx = re.compile(regex)
    rows = []
    for f in files:
        m = rx.search(Path(f).name)
        if not m:
            continue
        gsm, token, tp = m.group(1), m.group("token"), m.group("tp")
        token_key = token if token in cond_map else (
            "Fezf2KO" if "Fezf2KO" in token else
            "Fezf2Het_P1F" if "P1F" in token else
            "Fezf2Het_P1M" if "P1M" in token else
            "Fezf2Het" if "Fezf2Het" in token else
            "WT"
        )
        geno = cond_map[token_key]["genotype"]
        sex  = cond_map[token_key]["sex"]
        rows.append(dict(sample=f"{gsm}_{token}_{tp}",
                         gsm=gsm, token=token, timepoint=tp,
                         genotype=geno, sex=sex, file=f))
    return pd.DataFrame(rows)
