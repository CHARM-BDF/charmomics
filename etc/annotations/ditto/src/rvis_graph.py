import csv

import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

def savePlot(row):
    ditto_file = f'./data/results/rvis/ditto-genes/DITTO_{row["chrom"]}_{row["gene"]}.tsv'
    print(ditto_file)
    df = pd.read_csv(ditto_file, sep="\t", names=["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto"])

    print(df)
    plot_file = Path(f'./data/results/rvis/plots/{row["category"]}/DITTO_{row["chrom"]}_{row["gene"]}.png')
    plot_file.parent.mkdir(parents=True, exist_ok=True)

    plt.plot(df.index, df.ditto, linestyle='-', color='blue')
    plt.xlabel("Index", fontsize=10)
    plt.ylabel("Ditto Score", fontsize=10)

    plt.tick_params(axis='both', labelsize=8)
    
    plt.title(f"{row['chrom']} - {row['gene']} - RVIS score: {row['rvis_final']}", fontsize=8)
    plt.ticklabel_format(style='plain')
    
    plt.savefig(plot_file, dpi=300)
    plt.close()

    return

def main():
    rvis_gene_list = []

    rvis_graph_file = './data/results/rvis/rvis_graph.csv'
    rvis_headers = ["chrom", "gene", "category", "rvis_final"]

    with open(rvis_graph_file) as graph_file:
        csv_reader = csv.DictReader(
            graph_file,
            delimiter=",",
            fieldnames=rvis_headers
        )

        next(csv_reader)

        # temp_row = next(csv_reader)

        for row in csv_reader:
            print(row)
            savePlot(row)

    return


if __name__ == "__main__":
    main()