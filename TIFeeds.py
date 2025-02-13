

# URL to the raw .intel file in the source repository
#intel_file_url = "https://raw.githubusercontent.com/CriticalPathSecurity/Zeek-Intelligence-Feeds/refs/heads/master/compromised-ips.intel"
import csv
import pip._vendor.requests as requests
import os

# Base URL to the source repository (replace with the actual base URL)
base_url = "https://raw.githubusercontent.com/CriticalPathSecurity/Zeek-Intelligence-Feeds/refs/heads/master/"

# List of .intel files to process
intel_files = [
    "abuse-ch-malware.intel",
    "abuse-ch-threatfox-ip.intel",
    "compromised-ips.intel",
    "tweetfeed.intel"
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
        for line in lines:
            # Split the line by tabs (assuming the .intel file is tab-separated)
            row = line.split('\t')
            csv_writer.writerow(row)
            all_rows.append(row)  # Add the row to the all_rows list

    print(f"Converted {intel_file} to {csv_file_name}")

# Save all rows to a single all.csv file
with open("all.csv", mode='w', newline='', encoding='utf-8') as all_csv_file:
    csv_writer = csv.writer(all_csv_file)
    csv_writer.writerow(["indicator", "indicator_type", "meta.source", "meta.do_notice", "meta.desc"])  # Add header
    csv_writer.writerows(all_rows)  # Write all rows

print("Merged all CSV files into all.csv")
