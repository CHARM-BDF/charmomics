import argparse
import concurrent.futures
import csv
import json
import logging
import logging.config
import math
import multiprocessing as mp
import os
from statistics import quantiles
import subprocess

# Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

## Helper Functions ##
def statisticsStandardDeviation(gene, variants):
    """  """

    data_points = variants

    samples = len(data_points)
    
    sum = 0.0

    for data_point in data_points.values():
        value = float(data_point['ditto'])
        sum += value

    mean = sum / samples
    std_dev = 0.0

    for data_point in data_points.values():
        value = float(data_point['ditto'])
        std_dev += pow((value - mean), 2)

    std_dev = math.sqrt(std_dev / samples)

    match_count = samples

    stats = {
        'samples': samples,
        'sum': sum,
        'mean': mean,
        'std_dev': std_dev,
        'match_count': match_count
    }

    if std_dev == 0.0:
        return stats

    for data_point in data_points.values():
        value = float(data_point['ditto'])
        
        z = (value - mean) / std_dev
        
        if z < -2:
            # print(f"Data point: {value}; Z Score: {z} ")
            match_count -= 1
    
    stats['match_count'] = match_count

    logger.info(f"")
    logger.info(f"Gene: {gene}")
    logger.info(f"=================================")
    logger.info(f"Samples:            {samples}")
    logger.info(f"Sum:                {sum}")
    logger.info(f"Mean:               {mean}")
    logger.info(f"Standard Deviation: {std_dev}")
    logger.info(f"Match Count:        {match_count}")

    return stats

def statisticsQuartiles(gene, variants):
    """  """

    data_points = [float(variant['ditto']) for variant in variants.values()]
    
    quartiles = quantiles(data_points, n=4)

    samples = len(data_points)
    q1 = quartiles[0]
    q2 = quartiles[1]
    q3 = quartiles[2]

    logger.info(f"")
    logger.info(f"Gene: {gene}")
    logger.info(f"=================================")
    logger.info(f"Samples:            {samples}")
    logger.info(f"Q1:                 {q1}")
    logger.info(f"Q2:                 {q2}")
    logger.info(f"Q3:                 {q3}")
    
    stats = {
        'samples': samples,
        'first_quartile': q1,
        'second_quartile': q2,
        'third_quartile': q3
    }

    return stats

def fetchDittoVariants(ditto_base_path, meta_dict):
    """ """
    chrom = meta_dict['chrom']
    gene = meta_dict['gene']

    ditto_path = ditto_base_path + f"/tabix/{chrom}/DITTO_{chrom}_{gene}.tsv.gz"

    low = meta_dict['metadata']['low']
    high = meta_dict['metadata']['high']

    pos = low

    tabix_command = f'tabix {ditto_path} {chrom}:{low}-{high}'
    logger.info(f"  {tabix_command}")

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

    logger.info(f"  {len(meta_dict['variants'])}")

    return

## Step 1: Gather metadata information on Ditto gene files ##

# Step 1: Helper functions
def create_gene_metadata_entry(file_path, ditto_meta):
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
        'stats': {},
        'variants': {}
    }

    ditto_meta.setdefault(chrom_key, {}).setdefault(gene_key, (temp_dict))

    return

# Step 1 MetaData function
def metadata(metadata_file, ditto_file_paths):
    """ """
    logger.info("[Step 1]: Open metadata file as a python dictionary")
    with open(metadata_file, 'r') as ditto_meta_file:
            ditto_meta_dict = json.load(ditto_meta_file)

    logger.info("[Step 1]: For each gene file in DITTO parse into a python dictionary")
    for ditto_path in ditto_file_paths:
        if 'UNKNOWN' in ditto_path:
            continue

        create_gene_metadata_entry(ditto_path, ditto_meta_dict)

    logger.info(f"[Step 1]: Save ditto gene metadata to {metadata_file}")
    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(ditto_meta_dict, ditto_meta_file, indent=4)
    
    logger.info("[Step 1]: Done!")

## Step 2: Match ClinVar to precomputed Ditto scores ##

# Step 2: Helper Functions
def variant_type(ref, alt):
    """ Determines the variant type: SNV; INS; DEL; INDEL """

    if len(ref) == 1 and len(alt) > 1:
        return 'INS'
    elif len(ref) > 1 and len(alt) == 1:
        return 'DEL'
    elif len(ref) > 1 and len(alt) > 1:
        return 'INDEL'

    return 'SNV'

def findGeneByPosition(meta_dict, chrom, pos):
    """ Find with DITTO gene file to query using the metadata range """
    
    for gene in meta_dict[chrom].keys():
        if meta_dict[chrom][gene]['metadata']['low'] <= int(pos) <= meta_dict[chrom][gene]['metadata']['high']:
            return gene

    return None

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
    logger.info(f"  {tabix_command}")
    
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

# Step 2: Clinvar Match main function
def clinvar_match(ditto_base_path, metadata_file, clinvar_base_path, chromosome):
    """ """
    
    clinvar_plp_file = f'clinvar_{chromosome}_plp.tsv'
    clinvar_plp_path = clinvar_base_path + clinvar_plp_file

    logger.info(f"[Step 2]: Opening ClinVar file {clinvar_plp_path}")
    with open(clinvar_plp_path, mode='r') as file:
        data_lines = [line for line in file if not (line.startswith("##") or line.startswith("#"))]

    logger.info(f"[Step 2]: Creating a csv_reader from the ClinVar file")
    csv_reader = csv.DictReader(
            data_lines,
            delimiter='\t',
            fieldnames=["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
        )
    
    logger.info(f"[Step 2]: Opening the {metadata_file}")
    with open(metadata_file, 'r') as ditto_meta_file:
        meta_dict = json.load(ditto_meta_file)

    logger.info(f"[Step 2]: For each row in {clinvar_plp_file} find the precomputed Ditto score if it exists")
    for record in csv_reader:
        type = variant_type(record['REF'], record['ALT'])
        gene = findGeneByPosition(meta_dict, "chr" + record['CHROM'], record['POS'])

        if not gene:
            continue

        if not meta_dict:
            continue

        logger.info(f"  {record['CHROM']}-{record['POS']}-{record['REF']}-{record['ALT']} :: {gene} :: {type}")

        fetchDittoScores(ditto_base_path, meta_dict, record['CHROM'], gene, record['POS'], record['REF'], record['ALT'], type)
        
    logger.info(f"[Step 2]: Saving the results of the score fetching to {metadata_file}")
    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(meta_dict, ditto_meta_file, indent=4)
    
    logger.info(f"[Step 2]: Done!")

    return

## Step 3 - Perform statistics on Ditto ##

# Step 3 - Helper Functions
def worker(package):
    """ """
    
    ditto_base_path, meta_dict = package

    process_name = mp.current_process().name    
    
    logger.info(f"[Step 3]: [{process_name}] :: Opening {ditto_base_path}")
    if not meta_dict['clinvar']:
        fetchDittoVariants(ditto_base_path, meta_dict)

    logger.info(len(meta_dict['variants']))

    try:
        meta_dict['stats']['standard_deviation'] = statisticsStandardDeviation(meta_dict['gene'], meta_dict['variants'])
        meta_dict['stats']['quartiles'] = statisticsQuartiles(meta_dict['gene'], meta_dict['variants'])
    except Exception as e:
            logger.info(f"[Step 3]: EXCEPTION :: {e}")

    if meta_dict['clinvar']:
        logger.info(f"[Step 3]: [{process_name}] :: ClinVar Baby!!")
        
    meta_dict['variants'] = {}

    logger.info(f"[Step 3]: [{process_name}] :: {meta_dict}")

    return meta_dict

# Step 3 - Perform statistics on Ditto
def statistics(ditto_base_path, metadata_file, chromosome):
    """ """
    logger.info(f"[Step 3]: Opening and loading {metadata_file} into a python dict")
    with open(metadata_file, 'r') as ditto_meta_file:
            meta_dict = json.load(ditto_meta_file)

    logger.info(f"[Step 3]: Starting multiprocess Ditto variant fetcher")
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        try:
            jobs = executor.map(worker, [(ditto_base_path, meta_dict[chromosome][gene]) for gene in meta_dict[chromosome].keys()])

            for job in jobs:
                logger.info(f"[Step 3]: Cleanup, deleting job... {job}")

                chrom = job['chrom']
                gene = job['gene']

                meta_dict[chrom][gene] = job
        
        except Exception as e:
            logger.info(f"[Step 3]: EXCEPTION :: {e}")

    logger.info(f"[Step 3]: Saving meta dict to {metadata_file}...")
    with open(metadata_file, 'w') as ditto_meta_file:
        json.dump(meta_dict, ditto_meta_file, indent=4)

    logger.info(f"[Step 3]: Done!")

def main(args):
    """ """

    ## ARGS ##
    ditto_base_path = args.ditto
    clinvar_base_path = args.clinvar

    chromosome = f"chr{args.chromosome}"

    metadata_file = args.output + f"ditto_meta_data_{chromosome}.json"

    ## Steps ##
    # 0: Setup
    print("[ MAIN ] :: Step 0 :: Ditto filter setup")
    ditto_full_path = f'{ditto_base_path}/raw/{chromosome}/'
    ditto_file_paths = [ditto_full_path + file for file in os.listdir(ditto_full_path)]

    # Ensure the meta data file is created
    try:
        with open(metadata_file, 'x') as file:
            file.write(json.dumps({}))
    except FileExistsError:
        logger.info(f"The file '{metadata_file}' already exists.")

    # 1: Gather metadata information on Ditto gene files
    logger.info("[ MAIN ] :: Step 1 :: Gathering Metadata")
    metadata(metadata_file, ditto_file_paths)
    
    # 2: Match ClinVar to Ditto and get statistics
    logger.info("[ MAIN ] :: Step 2 :: Fetching scores for ClinVar Path/Likely Path variants")
    clinvar_match(ditto_base_path, metadata_file, clinvar_base_path, chromosome)
    
    # # 3: Perform statistics
    logger.info("[ MAIN ] :: Step 3 :: Perform statistics on DITTO")
    statistics(ditto_base_path, metadata_file, chromosome)

    logger.info("[ MAIN ] :: Done!")

    return

if __name__ == "__main__":
    """ """
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--ditto')
    parser.add_argument('-chr', '--chromosome')
    parser.add_argument('-cl', '--clinvar', default='./data/interim/clinvar_chrom_plp/')
    parser.add_argument('-o', '--output', default='./data/results/')

    args = parser.parse_args()
    
    main(args)
