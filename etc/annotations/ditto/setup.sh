#!/usr/bin/env bash

## Variable setup

# DITTO local data directory
DATA_DIR='data'

# Base URLs
CLINVAR_BASE="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38"

## Make directories
mkdir "$DATA_DIR" "$DATA_DIR/external" "$DATA_DIR/interim" "$DATA_DIR/results"
echo "[INFO] Making directories: ./$DATA_DIR/external; ./$DATA_DIR/interim; ./$DATA_DIR/results complete..."

## Download data files
echo "[NCBI]: Downloading 'clinvar.vcf.gz'"
curl -fSL --progress-bar  --retry 3 "$CLINVAR_BASE/clinvar.vcf.gz" -o "$DATA_DIR/external/clinvar.vcf.gz"

echo "[NCBI]: Downloading 'clinvar.vcf.gz.tbi'"
curl -fSL --progress-bar  --retry 3 "$CLINVAR_BASE/clinvar.vcf.gz.tbi" -o "$DATA_DIR/external/clinvar.vcf.gz.tbi"

echo "[INFO] Download complete..."

## Splitting out ClinVar into chromosomes to match with DITTO
if command -v bcftools &> /dev/null; then
    echo "[INFO] Splitting out ClinVar by Chromosome..."
    mkdir -p "$DATA_DIR/interim/clinvar_chrom_plp"

    echo -n "[BCFTOOLS] Splitting out ClinVar Variants marked Pathogenic/Likely Pathogenic on Chromosome"
    
    for i in {1..24}
    do
        if [[ "$i" == "23" ]]; then
            i="X"
        elif [[ "$i" == "24" ]]; then
            i="Y"
        fi

        echo -n " $i "
        bcftools view -r $i -i 'INFO/CLNSIG="Pathogenic" | INFO/CLNSIG="Likely_pathogenic"' "./$DATA_DIR/external/clinvar.vcf.gz" -o "$DATA_DIR/interim/clinvar_chrom_plp/clinvar_chr${i}_plp.tsv"
        
    done
else
    echo "bcftools could not be found, could not split out ClinVar."
    echo "To install bcftools, please visit and install: https://www.htslib.org/download/"
fi

echo ""
echo "[INFO] CHARMomics DITTO setup complete!"
