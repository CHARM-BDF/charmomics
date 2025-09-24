#! /bin/bash
# ./annotate-gene-list.sh -u https://dev.cgds.uab.edu/charmomics -f <gene_list_file_path.json>

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo " -u Base charmomics URL"
  echo "    (default) https://local.charmomics.cgds/charmomics"
  echo " -h Prints usage"
  echo " -f Provides the gene file list to queue annotations"
  echo " "
  echo "Kicks off annotation jobs in charmomics for a supplied list of genes to be annotated"
  echo " "
  echo "Note: This script may need to be run multiple times due to the charmomics"
  echo "annotation system not being built for large sets of annotations queued."
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

BASE_URL="https://local.charmomics.cgds/charmomics"
BASE_GENE_FILEPATH=""

while getopts ":u:hf:" opt; do
  case $opt in
    u) BASE_URL="$OPTARG";;
    h) usage;;
    f) BASE_GENE_FILEPATH="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if ! jq --version &> /dev/null
then
    echo "Error: jq could not be found. Exiting."
    usage
fi

if [ "$BASE_GENE_FILEPATH" = "" ]
then
  echo "Error: No gene file provided. Exiting"
  usage
fi

IFS=$'\n' read -d '' -r -a GENES < "$BASE_GENE_FILEPATH"

for gene in "${GENES[@]}"
do

    echo "Starting annotations for gene symbol $gene..."

    curl -s -X "POST" \
        "$BASE_URL/api/annotation/?type=gene&name=$gene" \
        -H "accept: application/json" \
        > /dev/null

    sleep 5

done
