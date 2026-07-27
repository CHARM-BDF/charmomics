#!/bin/bash

CHROMOSOME="$1"

SOURCE_PATH="/home/jscherer/Documents/ditto/genes/raw/chr$CHROMOSOME/"
DESTINATION_PATH="/home/jscherer/Documents/ditto/genes/tabix/chr$CHROMOSOME/"

mkdir -p $DESTINATION_PATH

for FILE_PATH in $(find $SOURCE_PATH -maxdepth 1 -type f); do

    FILE=$(basename "$FILE_PATH")

    echo "$DESTINATION_PATH$FILE"

    bgzip -k $FILE_PATH -o "$DESTINATION_PATH$FILE.gz"
    tabix -p vcf "$DESTINATION_PATH$FILE.gz"

done

echo "Done!"
