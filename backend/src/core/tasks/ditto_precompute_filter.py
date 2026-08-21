import logging
import vcfpy
import logging
import concurrent.futures
import csv
import os
import subprocess

import threading

class DittoPrecomputedFilter:
    def __init__(self, input_path, output_path, batch_size):
        self.chromosome_list = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10',
                        'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
                        'chr20', 'chr21', 'chr22', 'chrX', 'chrY']

        self.input_path = input_path
        self.output_path = output_path
        self.batch_size = batch_size

        self.logger = logging.getLogger()
        
        return
    
    ## Helper Functions ##
    def compute_variant_hash(self, chrom, pos, ref, alt, stage):
        if type(pos) is int:
            pos = str(pos)

        hash = chrom + pos + ref + alt

        return hash

    def build_dict_result(self, tabix_result):
        dict_result = {}
        
        csv_reader = csv.DictReader(
                tabix_result,
                delimiter='\t',
                fieldnames=["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]
            )

        for row in csv_reader:
            # logger.info(row)
            hash = self.compute_variant_hash(row['chrom'], row['pos'], row['ref'], row['alt'], "DITTO")
            dict_result.setdefault(hash, []).append(row)

        return dict_result

    def variant_type(ref, alt):
        """ Determines the variant type: SNV; INS; DEL; INDEL """

        if len(ref) == 1 and len(alt) > 1:
            return 'INS'
        elif len(ref) > 1 and len(alt) == 1:
            return 'DEL'
        elif len(ref) > 1 and len(alt) > 1:
            return 'INDEL'

        return 'SNV'

    def worker(self, batch):
        tabix_command = f'tabix /Users/jscherer/Desktop/ditto/{batch['chromosome']}.tsv.gz {batch['chromosome']}:{batch['low']}-{batch['high']}'.split(' ')

        result = subprocess.run(tabix_command, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

        ditto_dict_result = self.build_dict_result(result)
        ditto_records = []

        try:
            for record in batch['records']:

                # logger.info(record)
                ditto_result = False
                variant_hash = self.compute_variant_hash(record.CHROM, record.POS, record.REF, record.ALT[0].value, "RECORD")
                
                for transcript in ditto_dict_result[variant_hash]:
                    # logger.info(transcript)
                    if transcript['ref'] == record.REF and transcript['alt'] == record.ALT[0].value:
                        ditto_result = True
                        # logger.info(f"DITTO FOUND :: {record}")
                        ditto_records.append(record)
                        break
            
            if len(ditto_records) == 0:
                return None

            return ditto_records
        
        except KeyError as e:
            pass

    def batch_request(self, vcf_reader):
        batch = { "chromosome": "", "high": 0, "low": 0, "count": 0, "records": []}
        batch_list = []
        batch_num = 0
        self.batch_size = 10000

        for record in vcf_reader:
            if record.CHROM not in self.chromosome_list:
                continue
            if record.CHROM != batch['chromosome']:
                batch_num = 0
            if record.POS > batch_num:
                if len(batch['records']) > 0:
                    batch_list.append(batch)
                    batch['count'] = len(batch['records'])
                batch_num += self.batch_size
                batch = { "chromosome": record.CHROM, "high": 0, "low": record.POS, "count": 0, "records": [] }

            if record.POS > batch['high']:
                batch['high'] = record.POS
            batch['records'].append(record)

        return batch_list

    def run(self):
        with open(self.input_path, mode='r') as file:
            data_lines = [line for line in file if not (line.startswith("##") or line.startswith("#"))]

        csv_reader = csv.DictReader(
            data_lines,
            delimiter='\t',
            fieldnames=["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
        )

        vcf_writer = vcfpy.Writer.from_path(self.output_path, vcf_reader.header)

        batch_list = self.batch_request(vcf_reader)

        with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
            try:
                jobs = {executor.submit(self.worker, batch): batch for batch in batch_list}

                for job in concurrent.futures.as_completed(jobs):
                    
                    result = job.result()
                    
                    if result:
                        for row in result:
                            self.logger.info(row)
                            vcf_writer.write_record(row)

            except Exception as e:
                self.logger.info(f"MAIN :: EXCEPTION :: {e}")
