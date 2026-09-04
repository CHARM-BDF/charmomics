import csv
import math


def main():
    rvis_scores = []

    with open('./data/external/gnomAD_RVIS_Scores.csv') as rvis_file:
        rvis_headers = ["Gene","afr_y","amr_y","asj_y","eas_y","fin_y","nfe_y","sas_y","mutability","rvis_afr","rvis_eas","rvis_asj","rvis_nfe","rvis_sas","rvis_amr","rvis_fin"]

        csv_reader = csv.DictReader(
            rvis_file,
            delimiter=",",
            fieldnames=rvis_headers
        )

        # Skip header
        next(csv_reader) 

        for record in csv_reader:
            rvis_score = { 'gene': record['Gene'], 'final': float(record['rvis_fin']) }

            rvis_scores.append(rvis_score)

    rvis_scores = sorted(rvis_scores, key=lambda x: x['final'], reverse=True)

    print(len(rvis_scores))

    # Top

    print()
    print("Top Ten")
    top_ten = rvis_scores[:10]

    for score in top_ten:
        print(f"{score['gene']} :: {score['final']}")

    plotting(top_ten)

    # Middle

    print()
    print("Middle Ten")

    middle = math.ceil(len(rvis_scores) / 2)
    middle_low = middle - 5
    middle_high = middle + 5

    print(f"{middle_low} :: {middle} :: {middle_high}")

    middle_ten = rvis_scores[middle_low:middle_high]

    for score in middle_ten:
        print(f"{score['gene']} :: {score['final']}")

    # Bottom
    print()
    print("Bottom Ten")
    bottom_ten = rvis_scores[-10:]

    for score in bottom_ten:
        print(f"{score['gene']} :: {score['final']}")



if __name__ == "__main__":
    main()