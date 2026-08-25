#!/bin/bash
# shellcheck source=/dev/null

install_backend_service() {
    # Change to backend directory, if not exit
    cd backend || { echo "Failure to change to backend directory"; exit 1; }

    # Create and activate python venv
    python3 -m venv charmomics_env
    source charmomics_env/bin/activate

    # Install python requirements with pip
    pip3 install -r requirements.txt

    # Deactivate python venv and return to root directory, if not exit
    deactivate
    cd - || { echo "Unable to change return to root directory"; exit 1; }

    echo "Use 'source backend/charmomics_env/bin/activate' to activate the virtual environment"
}

install_tls_certificate() {
    # check if mkcert is installed, generates tls certificates if found
    if command -v mkcert &> /dev/null; then
        echo "mkcert found, generating certificates"
        ./etc/network/generate-ssl-certs.sh local.charmomics.cgds ./etc/network/.certificates
    else
        echo "mkcert could not be found, could not generate certificates. Browser will throw insecure warning."
        echo "To generate certificates, please visit and install: https://github.com/FiloSottile/mkcert"
    fi
}

download_datasets() {
    DATA_DIR='./backend/etc/data/'

    # Make directories
    mkdir -p "$DATA_DIR" "$DATA_DIR/external" "$DATA_DIR/interim" "$DATA_DIR/raw"

    CGDS_LTS_BASE="https://s3.lts.rc.uab.edu/cgds-public/charmomics"

    # NCBI data
    echo "[NCBI]: Downloading 'GCA_000001405.15_GRCh38_no_alt_analysis_set.fna"
    curl --progress-bar  --retry 3 -o "$DATA_DIR/external/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna" "$CGDS_LTS_BASE/bcftools/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna"

    echo "[NCBI]: Downloading 'GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.fai'"
    curl --progress-bar  --retry 3 -o "$DATA_DIR/external/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.fai" "$CGDS_LTS_BASE/bcftools/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.fai"

    # Gnomad data
    echo "[ECHTVAR]: Downloading 'gnomad.v3.1.2.echtvar.v2.zip'"
    curl --progress-bar --retry 3 -o "$DATA_DIR/external/gnomad.v3.1.2.echtvar.v2.zip" "$CGDS_LTS_BASE/echtvar/gnomad.v3.1.2.echtvar.v2.zip"

}

clean() {
    # Clean backend of virtual environment
    deactivate
    echo "Removing backend/charmomics_env/..."
    cd backend || { echo "Failure to change backend project directory"; exit 1; }
    rm -rf charmomics_env
    cd - || { echo "Failure to change return to root directory"; exit 1; }    
}

clean_option="clean"

if [[ $# -ne 0 ]] && [[ $1 -eq $clean_option ]]; then
    clean
fi

# check dns entry in hosts, adds if not present
./etc/network/etc-hosts.sh local.charmomics.cgds

# Install project requirements
install_tls_certificate

# Install services
install_backend_service

# Download Datasets
download_datasets