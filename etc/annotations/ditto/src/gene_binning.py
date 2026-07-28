import concurrent.futures
import csv
import fcntl
import logging
import logging.config
import multiprocessing as mp
import subprocess

# Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

fieldnames = ["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto" ]

def worker(tuple):
    logger.info("WORKER :: Starting worker...")
    try:
        queue, batch = tuple
        
        dittodb_path = '/Users/jscherer/Desktop/dittodb'

        tabix_command = f'tabix --verbosity 0 {dittodb_path}/DITTO_{batch["chromosome"]}.tsv.gz {batch["chromosome"]}:{batch["position"]}'.split(' ')
        
        print(' '.join([str(x) for x in tabix_command]))
        
        try:
            tabix_result = subprocess.run(tabix_command, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        except Exception as e:
            logger.info(f"WORKER :: EXCEPTION :: {e}")

        
        dict_result = {}
        csv_reader = csv.DictReader(tabix_result, delimiter='\t', fieldnames=fieldnames)

        for row in csv_reader:
            key = row['gene'] if row['gene'] != '' else 'UNKNOWN'
            dict_result.setdefault(key, []).append(row)

        for key, records in dict_result.items():
            queue.put((key, records, batch["chromosome"]))
    except Exception as e:
        logger.info(f"WORKER :: EXCEPTION :: {e}")

    return

def listener(index, queue):
    try:
        logger.info(f"LISTENER {index} :: Listener is running...")

        while 1:
            logger.info(f"LISTENER {index} :: Grabbing from Queue... Size :{queue.qsize()}:")
            item = queue.get()

            if item == "kill":
                break

            key, records, chromosome = item
            
            logger.info(f"LISTENER {index} :: {key} :: Queue size :{queue.qsize()}:")

            gene = f'{chromosome}_{key}'
            file_name = f"DITTO_{gene}.tsv"

            write_file_path = f'/Volumes/NVME-2TB/Work/ditto/gene/{chromosome}/{file_name}'
            # write_file_path = f'/Volumes/SATA-512GB/ditto-genes/{chromosome}/{file_name}'

            logger.info(f"LISTENER {index} :: Writing to {file_name}...")
            try:
                with open(write_file_path, 'a', newline='') as tsvfile:
                    fcntl.lockf(tsvfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
                    for record in records:
                        writer.writerow(record)
                    fcntl.lockf(tsvfile, fcntl.LOCK_UN)
            except (OSError, BlockingIOError):
                logger.info(f"LISTENER {index} :: {file_name} is already locked by another process")
                queue.put(item)
    except Exception as e:
        logger.info(f"LISTENER {index} :: EXCEPTION :: {e}")

    return

def main():
    ## VARIABLES ##
    batch_size = 7500
    max_queue_size = 10
    num_processes = 10
    num_listener = 8
    num_workers = 5
    
    # chromosome_list = {
    #     'chr1': 248946422, 'chr2': 242183529, 'chr3': 198235559, 'chr4': 190204555, 'chr5': 181478259,
    #     'chr6': 170745979, 'chr7': 159335973, 'chr8': 145078636, 'chr9': 138334717, 'chr10': 133787422,
    #     'chr11': 135076622, 'chr12': 133265309, 'chr13': 114354328, 'chr14': 106883718, 'chr15': 101981189,
    #     'chr16': 90228345, 'chr17': 83247441, 'chr18': 80263285, 'chr19': 58607616, 'chr20': 64334167,
    #     'chr21': 46699983, 'chr22': 50808468, 'chrX': 156030895, 'chrY': 57217415
    # }

    chromosome_list = { 'chrX': 156030895 }

    ## Batching ##    
    batch_num = 0
    batch_list = []

    for chromosome, size in chromosome_list.items():
        while batch_num <= size:
            batch = { 'chromosome': '', 'position': '', 'records': [] }
            low_pos = batch_num
            batch_num += batch_size
            high_pos = batch_num
            if batch_num > size:
                high_pos = size

            batch['chromosome'] = chromosome
            batch['position'] = f"{low_pos}-{high_pos}"
            batch_list.append(batch)

    ## Multiprocessing Start ##

    manager = mp.Manager()
    queue = manager.Queue(8)

    batch_list = [(queue, batch) for batch in batch_list]

    # Listeners
    listeners = []

    for index in range(num_listener):
        p = mp.Process(target=listener, args=(index, queue,))
        p.start()
        listeners.append(p)


    # Workers
    # workers = []

    # for index in range(num_workers):
    #     p = mp.Process(target=worker, args=((queue, batch_list[index]),))
    #     p.start()
    #     workers.append(p)

    with mp.Pool(processes=8) as pool:
        pool.map_async(worker, batch_list)

        pool.close()
        pool.join()
    
    [p.join() for p in listeners]

    # Listener pool #

    # # Worker pool #
    # with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
    #     try:
    #         jobs = {executor.submit(worker,(queue, batch)): batch for batch in batch_list}

    #         for job in concurrent.futures.as_completed(jobs):
    #             logger.info(f"MAIN :: Cleanup, deleting job... {job}")
    #             jobs.pop(job)
    #             gc.collect()
    #     except Exception as e:
    #         logger.info(f"MAIN :: EXCEPTION :: {e}")

    # Program is done, stop queue and listeners #

if __name__ == '__main__':
    main()
