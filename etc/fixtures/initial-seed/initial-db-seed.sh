#! /bin/bash
# ./initial-db-seed.sh -h <host> -f <datasource>

usage() {
  echo "usage: $0 -h <host> -f <datasource>"
  echo " "
  echo " -h MongoDB host URL"
  echo "    (default) localhost:27017"
  echo " -f Fixtures filepath"
  echo "    (default) /tmp/fixtures/initial-seed"
  echo " "
  echo "Seeds the initial Franklin database with base fixtures for local development and system testing"
  exit
}

while getopts ":a:v:h" opt; do
  case $opt in
    a) mongodb_host=$OPTARG;;
    v) fixture_filepath=${OPTARG};;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if [[ ! -v mongodb_host ]] ; then
  mongodb_host="localhost:27017"
fi

if [[ ! -v fixture_filepath ]] ; then
  fixture_filepath="/tmp/fixtures/initial-seed"
fi

echo "Seeding Franklin database..."

database="franklin_db"

echo "Importing Annotation Configuration file..."
mongoimport --db "$database" --collection annotation_config --file "$fixture_filepath/annotation-config.json" --jsonArray

echo "Seeding Franklin database...Complete"
