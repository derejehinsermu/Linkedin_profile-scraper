import csv

def export_to_csv(profile_urls, csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Profile URLs"])
        writer.writerows([[url] for url in profile_urls])
