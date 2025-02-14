import csv
import requests
import os

# Base URL to the source repository (replace with the actual base URL)
base_url = "https://raw.githubusercontent.com/CriticalPathSecurity/Zeek-Intelligence-Feeds/refs/heads/master/"

# List of .intel files containing domain indicators
intel_files = [
    "fangxiao.intel"
]

# List to store all rows from all CSV files
all_rows = []

# Process each .intel file
for intel_file in intel_files:
    # Fetch the .intel file
    intel_file_url = base_url + intel_file
    response = requests.get(intel_file_url)
    lines = response.text.splitlines()

    # Remove the header (first line)
    lines = lines[1:]

    # Convert to CSV and save
    csv_file_name = os.path.splitext(intel_file)[0] + ".csv"  # Replace .intel with .csv
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header for the CSV
        csv_writer.writerow(["indicator", "indicator_type", "meta.source", "meta.do_notice", "meta.desc"])

        for line in lines:
            # Split the line by tabs (assuming the .intel file is tab-separated)
            row = line.split('\t')
            # Check if the row contains enough columns
            if row and len(row) >= 5:
                indicator = row[0]
                indicator_type = row[1] if len(row) > 1 else ""
                meta_source = row[2] if len(row) > 2 else ""
                meta_do_notice = row[3] if len(row) > 3 else ""
                meta_desc = row[4] if len(row) > 4 else ""

                # Check if the indicator is a valid domain (you can customize this further based on format)
                if '.' in indicator and not indicator.startswith('http'):  # Basic check for domain
                    # Write the row to the CSV file
                    csv_writer.writerow([indicator, indicator_type, meta_source, meta_do_notice, meta_desc])

                    # Store in the all_rows list for the merged CSV
                    all_rows.append([indicator, indicator_type, meta_source, meta_do_notice, meta_desc])

    print(f"Converted {intel_file} to {csv_file_name}")

# Save all rows to a single all_domains.csv file
with open("all_domains.csv", mode='w', newline='', encoding='utf-8') as all_csv_file:
    csv_writer = csv.writer(all_csv_file)
    # Add the header for the merged file
    csv_writer.writerow(["indicator", "indicator_type", "meta.source", "meta.do_notice", "meta.desc"])
    # Write all rows
    csv_writer.writerows(all_rows)

print("Merged all domains into all_domains.csv")
