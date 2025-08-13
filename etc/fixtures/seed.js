// connection URI
const uri = 'mongodb://localhost:27017/charmomics_db';

// The default path to the fixtures, can be changed to a script argument in the future
const fixturePath = '/tmp/fixtures';

// This JavaScript executes within a mongosh shell making 'connect' is implicitly available
const db = connect(uri); // eslint-disable-line no-undef

const collections = {
  'annotation_config': require(`${fixturePath}/initial-seed/annotation-config.json`),
};

const addCollections = ['annotation_config'];
const dropCollections = ['annotation_config', 'genomic_units', 'annotation_manifest'];

try {
  console.log(`Connected to MongoDB with URI ${uri}`);

  for ( const collectionName of dropCollections ) {
    db[collectionName].drop();
    print(`Dropping [${collectionName}] collection...`);
  }

  for ( const collectionName of addCollections ) {
    db[collectionName].insertMany(collections[collectionName]);
    print(`Seeding [${collectionName}] with ${db[collectionName].countDocuments()} documents...`);
  }
} catch (err) {
  console.log(err.stack);
}