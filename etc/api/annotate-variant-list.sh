#! /bin/bash
# ./annotate-variant-list.sh -u https://dev.cgds.uab.edu/charmomics -f <variant_list_file_path.json>

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo " -u Base charmomics URL"
  echo "    (default) https://local.charmomics.cgds/charmomics"
  echo " -h Prints usage"
  echo " -f Provides the variant file list to queue annotations"
  echo " "
  echo "Kicks off annotation jobs in charmomics for a supplied list of variants to be annotated"
  echo " "
  echo "Note: This script may need to be run multiple times due to the charmomics"
  echo "annotation system not being built for large sets of annotations queued."
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
  exit
}

BASE_URL="https://local.charmomics.cgds/charmomics"
BASE_VARIANT_FILEPATH=""

while getopts ":u:hf:" opt; do
  case $opt in
    u) BASE_URL="$OPTARG";;
    h) usage;;
    f) BASE_VARIANT_FILEPATH="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if ! jq --version &> /dev/null
then
  echo "Error: jq could not be found. Exiting."
  usage
fi

if [ "$BASE_VARIANT_FILEPATH" = "" ]
then
  echo "Error: No variant file provided. Exiting"
  usage
fi

IFS=$'\n' read -d '' -r -a VARIANTS < "$BASE_VARIANT_FILEPATH"

for variant in "${VARIANTS[@]}"
do

    echo "Starting annotations for variant symbol $variant..."

    curl -s -X "POST" \
        "$BASE_URL/api/annotation/?type=hgvs_variant&name=$variant" \
        -H "accept: application/json" \
        > /dev/null

    sleep 5

done
