CHROMOSOME="$1"

BASE_PATH="/home/$USER/Documents/ditto/genes/raw/chr$CHROMOSOME/"

for FILEPATH in $(find $BASE_PATH -maxdepth 1 -type f); do  
    BASE_FILE_PATH="$FILEPATH"
    SORTED_FILE_PATH=""$FILEPATH"_sorted"

    echo $BASE_FILE_PATH
    echo $SORTED_FILE_PATH
    echo ""

    # $(sort -n -t$'\t' -k2,2 $BASE_FILE_PATH > $SORTED_FILE_PATH)
    $(sort -k1,1 -k2,2 $BASE_FILE_PATH > $SORTED_FILE_PATH)
    rm $BASE_FILE_PATH
    mv $SORTED_FILE_PATH $BASE_FILE_PATH

done

echo "Done!"
