import csv

if __name__ == "__main__":

    dup = {}
    with open("df_sorted.csv", "r") as csv_file:
        with open("df_sorted_no_dups.csv", "w") as output_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:

                if not dup.get(row["name"], False):
                    writer.writerow(row)
                    dup[row["name"]] = True
