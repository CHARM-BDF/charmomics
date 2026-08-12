import argparse
import concurrent.futures
import csv
import json
import logging
import logging.config
import os

from pathlib import Path

# Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def read_ditto_tsv(path, work_dict):
    with open(path, 'r') as gene_file:
        ditto_tsv_fieldnames = ["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
        csv_reader = csv.DictReader( gene_file, delimiter='\t', fieldnames=ditto_tsv_fieldnames)

        for row in csv_reader:
            hash = ' '.join((row['chrom'], row['pos'], row['ref'], row['alt']))

            temp_variant = work_dict['variants'].get(hash)

            if temp_variant:
                if float(row['ditto']) > temp_variant:
                    work_dict['variants'][hash] = temp_variant
            else:
                work_dict['variants'][hash] = float(row['ditto'])

    return

def ditto_filter(meta_dict, work_dict):
    # cutOff = 0.86 if meta_dict['clinvar'] else batch['cutOff']

    for key, value in work_dict['variants'].items():
        if meta_dict['stats']['std_dev'] == 0.0:
            work_dict['keep'].append(key)
        else
            z = (value - meta_dict['stats']['mean']) / meta_dict['stats']['std_dev']
            if z >= -2:
                work_dict['keep'].append(key)

    return

def write(input_file_path, output_file_path, meta_dict, work_dict):
    logger.info(f"WORKER :: {meta_dict['chrom']}:{meta_dict['gene']} :: Originally {len(work_dict['variants'])} and writing out {len(work_dict['keep'])} variants...")

    with open(input_file_path, 'r') as gene_file:
        ditto_tsv_fieldnames = ["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
        csv_reader = csv.DictReader( gene_file, delimiter='\t', fieldnames=ditto_tsv_fieldnames)
        
        with open(output_file_path, 'a', newline='') as f:
            fieldnames = ["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')

            for row in csv_reader:
                hash = ' '.join((row['chrom'], row['pos'], row['ref'], row['alt']))

                if hash in work_dict['keep']:
                    writer.writerow(row)

    return

def worker(input_path, output_path, meta_dict):

    # DITTO_chrY_ABCB7
    file = f"DITTO_{meta_dict['chrom']}_{meta_dict['gene']}"

    # /Volumes/SATA-512GB/workspace/ditto/genes/raw/chrY
    input_file_path = input_path + file + ".tsv"

    # data/results/chrY
    output_file_path = output_path + file + ".tsv"

    os.makedirs(output_path, exist_ok=True)

    work_dict = { 'keep': [], 'variants': {} }

    logger.info(f"[WORKER] :: Input File {input_file_path} -:- Output File {output_file_path}")

    try:
        read_ditto_tsv(input_file_path, work_dict)
        ditto_filter(meta_dict, work_dict)
        work_dict['keep'] = set(work_dict['keep'])
        write(input_file_path, output_file_path, meta_dict, work_dict)
    except Exception as e:
            logger.info(f"WORKER :: EXCEPTION :: {e}")

    return

def main(args):
    logger.info(args)

    # Setup Variables
    chromosome = f"chr{args.chromosome}"

    input_path = args.ditto.removesuffix('/') + f"/raw/{chromosome}/"
    metadata_file = args.meta + f'ditto_meta_data_{chromosome}.json'
    output_path = args.output.removesuffix('/') + f"/{chromosome}/"
    
    logger.info(chromosome)
    logger.info(input_path)
    logger.info(metadata_file)
    logger.info(output_path)

    with open(metadata_file, 'r') as file:
        metadata = json.load(file)
    
    # for key in metadata[chromosome].values():
    #     logger.info(key)

    # meta_dict =  {'gene': 'RNU1-107P', 'chrom': 'chrY', 'clinvar': False, 'metadata': {'low': 25721342, 'high': 25725495, 'range': 4153}, 'stats': {'samples': 12466, 'sum': 5.554448487348328, 'mean': 0.00044556782346769834, 'std_dev': 0.0007371403903963966, 'leftover_count': 12466}, 'variants': {}}
    # worker(input_path, output_path, meta_dict)

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        try:
            jobs = {
                executor.submit(worker, input_path, output_path, meta_dict): meta_dict for meta_dict in metadata[chromosome].values()
            }

            for job in concurrent.futures.as_completed(jobs):
                # logger.info(f"MAIN :: Cleanup, deleting job... {job}")
                jobs.pop(job)

        except Exception as e:
            logger.info(f"MAIN :: EXCEPTION :: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-chr', '--chromosome')
    parser.add_argument('-d', '--ditto')
    parser.add_argument('-m', '--meta', default="./data/results/")
    parser.add_argument('-o', '--output', default="./data/results/filtered/")

    args = parser.parse_args()

    main(args)