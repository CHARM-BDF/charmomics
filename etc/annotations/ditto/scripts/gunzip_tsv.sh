#!/bin/bash

CHROMOSOME="chr$1"

SOURCE_PATH="/Volumes/SATA-512GB/workspace/ditto/dittodb/$CHROMOSOME/"

DESTINATION_PATH="/Volumes/SATA-512GB/workspace/ditto/dittodb/$CHROMOSOME/"

mkdir -p $DESTINATION_PATH

for FILE_PATH in $(find $SOURCE_PATH -maxdepth 1 -type f); do

    FILE=$(basename "$FILE_PATH")
    NEW_FILE=$(basename "$FILE_PATH" .gz)

    echo "$DESTINATION_PATH$NEW_FILE"

    gunzip -c $FILE_PATH  > "$DESTINATION_PATH$NEW_FILE"

done

echo "Done!"
