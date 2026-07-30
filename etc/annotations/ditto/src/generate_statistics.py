import argparse
import concurrent.futures
import csv
import json
import logging
import logging.config
import math
import multiprocessing as mp
import os
import subprocess

# Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

## Helper Functions ##
def parse_tsv_to_dict(file_path, ditto_meta):
    ditto_tsv_fieldnames = ["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
    
    first_row = None
    last_row = None

    with open(file_path, 'r') as gene_file:
        csv_reader = csv.DictReader(gene_file, delimiter='\t', fieldnames=ditto_tsv_fieldnames)
        first_row = next(csv_reader) 
    
    with open(file_path, 'rb') as f:
        try:
            # Jump to the end of the file
            f.seek(-2, os.SEEK_END)
            # Read backward until we hit a newline character
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            # Handle files with only one line or empty files
            f.seek(0)
            
        last_line = f.readline().decode('utf-8')
        
        last_row = next(csv.DictReader([last_line], delimiter='\t', fieldnames=ditto_tsv_fieldnames))
        
    if not first_row or not last_row:
        return

    chrom_key = first_row['chrom']
    gene_key = first_row['gene']

    temp_dict = {
        'gene': first_row['gene'],
        'chrom': first_row['chrom'],
        'clinvar': False,
        'metadata': {
            'low': int(first_row['pos']),
            'high': int(last_row['pos']),
            'range': int(last_row['pos']) - int(first_row['pos'])
        },
        'stats': {
            'samples': 0,
            'sum': 0,
            'mean': 0.0,
            'std_dev': 0.0,
            'leftover_count': 0
        },
        'variants': {}
    }

    ditto_meta.setdefault(chrom_key, {}).setdefault(gene_key, (temp_dict))

    return

def findGeneByPosition(meta_dict, chrom, pos):
    """ Find with DITTO gene file to query using the metadata range """
    
    for gene in meta_dict[chrom].keys():
        if meta_dict[chrom][gene]['metadata']['low'] <= int(pos) <= meta_dict[chrom][gene]['metadata']['high']:
            return gene

    return None

def variant_type(ref, alt):
    """ Determines the variant type: SNV; INS; DEL; INDEL """

    if len(ref) == 1 and len(alt) > 1:
        return 'INS'
    elif len(ref) > 1 and len(alt) == 1:
        return 'DEL'
    elif len(ref) > 1 and len(alt) > 1:
        return 'INDEL'

    return 'SNV'

def fetchDittoScores(ditto_base_path, meta_dict, chrom, gene, pos, ref, alt, type):
    """ """
    ditto_path = ditto_base_path + f"/tabix/chr{chrom}/DITTO_chr{chrom}_{gene}.tsv.gz"

    if type == "INS":
            pos = str(int(pos) + 1)
            ref = '-'
            alt = alt[1:]
    if type == "DEL":
            pos = str(int(pos) + 1)
            ref = ref[1:]
            alt = '-'

    tabix_command = f'tabix {ditto_path} chr{chrom}:{pos}-{pos}'
    print(tabix_command)
    
    tabix_result = subprocess.run(tabix_command.split(' '), stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

    csv_reader = csv.DictReader(
            tabix_result,
            delimiter='\t',
            fieldnames=["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
        )
    
    match = False
    temp_variant = {}

    for row in csv_reader:
        if row['pos'] == pos and row['ref'] == ref and row['alt'] == alt:
            
            hash = ' '.join((f'chr{chrom}', pos, ref, alt))
            match = True

            ditto_score = temp_variant.get('ditto')
            
            if not ditto_score:
                temp_variant = row
                continue
            
            if row['ditto'] > ditto_score:
                temp_variant = row

    if match:
        # print("Match!")
        meta_dict[f'chr{chrom}'][gene]['variants'][hash] = temp_variant
        meta_dict[f'chr{chrom}'][gene]['clinvar'] = True

    return

def dictStats(meta_dict):
    """  """

    meta_dict['stats']['samples'] = len(meta_dict['variants'].keys())
    
    for hash in meta_dict['variants'].keys():
        meta_dict['stats']['sum'] += float(meta_dict['variants'][hash]['ditto'])

    meta_dict['stats']['mean'] = meta_dict['stats']['sum'] / meta_dict['stats']['samples']

    for hash in meta_dict['variants'].keys():
        score = float(meta_dict['variants'][hash]['ditto'])
        meta_dict['stats']['std_dev'] += math.pow((score - meta_dict['stats']['mean']), 2)
    
    meta_dict['stats']['std_dev'] = math.sqrt(meta_dict['stats']['std_dev'] / meta_dict['stats']['samples'])

    if meta_dict['stats']['std_dev'] == 0.0:
        meta_dict['stats']['leftover_count'] = 1
        meta_dict['variants'] = {}
        return

    scores_keep = []

    for hash in meta_dict['variants'].keys():
        score = float(meta_dict['variants'][hash]['ditto'])
        z = (score - meta_dict['stats']['mean']) / meta_dict['stats']['std_dev']

        if z >= -4:
            scores_keep.append(score)

    meta_dict['stats']['leftover_count'] = len(scores_keep)
    
    meta_dict['variants'] = {}

    return

def saveMetaDict(metadata_file, meta_dict):
    """ """
    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(meta_dict, ditto_meta_file, indent=4)

def fetchDittoVariants(ditto_base_path, meta_dict):
    """ """
    chrom = meta_dict['chrom']
    gene = meta_dict['gene']

    ditto_path = ditto_base_path + f"/tabix/{chrom}/DITTO_{chrom}_{gene}.tsv.gz"

    low = meta_dict['metadata']['low']
    high = meta_dict['metadata']['high']

    pos = low

    tabix_command = f'tabix {ditto_path} {chrom}:{low}-{high}'
    print(tabix_command)

    tabix_result = subprocess.run(tabix_command.split(' '), stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

    csv_reader = csv.DictReader(
        tabix_result,
        delimiter='\t',
        fieldnames=["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
    )

    for row in csv_reader:
        hash = ' '.join((row['chrom'], row['pos'], row['ref'], row['alt']))
        
        temp_variant = meta_dict['variants'].get(hash)

        if temp_variant:
            if row['ditto'] > temp_variant['ditto']:
                meta_dict['variants'][hash] = temp_variant
        else:
            meta_dict['variants'][hash] = row

    print(len(meta_dict['variants']))

    return

def worker(package):
    """ """
    ditto_base_path, meta_dict = package

    print(ditto_base_path)
    print(meta_dict)

    if meta_dict['clinvar']:
        print("CLINVAR BABY!!")
        meta_dict['variants'] = {}

    if not meta_dict['clinvar']:
        fetchDittoVariants(ditto_base_path, meta_dict)

    dictStats(meta_dict)    

    return meta_dict

# Step 1: Gather metadata information on Ditto gene files
def metadata(metadata_file, ditto_file_paths):
    """ """
    with open(metadata_file, 'r') as ditto_meta_file:
            ditto_meta_dict = json.load(ditto_meta_file)

    for ditto_path in ditto_file_paths:
        if 'UNKNOWN' in ditto_path:
            continue

        parse_tsv_to_dict(ditto_path, ditto_meta_dict)

    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(ditto_meta_dict, ditto_meta_file, indent=4)

# Step 2: Match ClinVar to Ditto and get statistics
def clinvar(ditto_base_path, metadata_file, clinvar_base_path, chromosome):
    """ """
    clinvar_plp_path = clinvar_base_path + f'clinvar_{chromosome}_plp.tsv'

    with open(clinvar_plp_path, mode='r') as clinvar_plp_file:
        data_lines = [line for line in clinvar_plp_file if not (line.startswith("##") or line.startswith("#"))]

    clinvar_header = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
    csv_reader = csv.DictReader(
            data_lines,
            delimiter='\t',
            fieldnames=clinvar_header
        )
    
    with open(metadata_file, 'r') as ditto_meta_file:
        meta_dict = json.load(ditto_meta_file)

    for record in csv_reader:
        type = variant_type(record['REF'], record['ALT'])
        gene = findGeneByPosition(meta_dict, "chr" + record['CHROM'], record['POS'])

        if not gene:
            continue

        if not meta_dict:
            continue

        print(f"{record['CHROM']}-{record['POS']}-{record['REF']}-{record['ALT']} :: {gene} :: {type}")

        fetchDittoScores(ditto_base_path, meta_dict, record['CHROM'], gene, record['POS'], record['REF'], record['ALT'], type)
        
    # Save the result
    saveMetaDict(metadata_file, meta_dict)

def savePartialMetaDict(metadata_file, meta_dict):
    """ """
    print(f"SAVING PARTIAL DICT TO FILE!! :: {meta_dict['gene']}")
    with open(metadata_file, 'r') as ditto_meta_file:
        ditto_meta_dict = json.load(ditto_meta_file)

    chrom = meta_dict['chrom']
    gene = meta_dict['gene']

    ditto_meta_dict[crom][gene] = meta_dict

    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(ditto_meta_dict, ditto_meta_file, indent=4)

# Step 3 - Perform statistics on Ditto
def statistics(ditto_base_path, metadata_file, chromosome):
    """ """
    with open(metadata_file, 'r') as ditto_meta_file:
            meta_dict = json.load(ditto_meta_file)

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        try:
            jobs = executor.map(worker, [(ditto_base_path, meta_dict[chromosome][gene]) for gene in meta_dict[chromosome].keys()])

            for job in jobs:
                logger.info(f"MAIN :: Cleanup, deleting job... {job}")

                chrom = job['chrom']
                gene = job['gene']

                meta_dict[chrom][gene] = job
        
        except Exception as e:
            logger.info(f"MAIN :: EXCEPTION :: {e}")

    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(meta_dict, ditto_meta_file, indent=4)

def main(args):
    """ """

    ## ARGS ##
    ditto_base_path = args.ditto
    clinvar_base_path = args.clinvar
    metadata_file = args.output

    chromosome = f"chr{args.chromosome}"

    ## Steps ##
    # 0: Setup
    print("Step 0: Ditto filter setup")
    ditto_full_path = f'{ditto_base_path}/raw/{chromosome}/'
    ditto_file_paths = [ditto_full_path + file for file in os.listdir(ditto_full_path)]

    # Ensure the meta data file is created
    try:
        with open(metadata_file, 'x') as file:
            file.write(json.dumps({}))
    except FileExistsError:
        print(f"The file '{metadata_file}' already exists.")

    # 1: Gather metadata information on Ditto gene files
    print("Step 1: Gathering Metadata")
    metadata(metadata_file, ditto_file_paths)
    
    # 2: Match ClinVar to Ditto and get statistics
    print("Step 2: Fetching scores for ClinVar Path/Likely Path variants and running statistics")
    clinvar(ditto_base_path, metadata_file, clinvar_base_path, chromosome)
    
    # 3: Perform statistics
    print("Step 3: Perform statistics on DITTO")
    statistics(ditto_base_path, metadata_file, chromosome)

    return

if __name__ == "__main__":
    """ """
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--ditto')
    parser.add_argument('-chr', '--chromosome')
    parser.add_argument('-cl', '--clinvar', default='./data/interim/clinvar_chrom_plp/')
    parser.add_argument('-o', '--output', default='./data/results/ditto_meta_data.json')

    args = parser.parse_args()
    
    main(args)

