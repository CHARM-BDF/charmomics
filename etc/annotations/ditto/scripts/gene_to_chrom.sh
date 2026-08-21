CHROMOSOME="$1"

SOURCE_PATH="/home/$USER/Documents/ditto/genes/filtered/chr$CHROMOSOME/"
DESTINATION_FILE="/data/project/worthey_lab/projects/experimental_pipelines/james/ditto/chromosome/filtered/ditto_filtered_chr$CHROMOSOME.tsv"

touch $DESTINATION_FILE

for FILE in $(find $SOURCE_PATH -maxdepth 1 -type f); do
	cat "$FILE" >> "$DESTINATION_FILE"
done

echo "Done!"