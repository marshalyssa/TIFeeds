import csv
import pip._vendor.requests as requests

# URL to the raw .intel file in the source repository
intel_file_url = "https://raw.githubusercontent.com/CriticalPathSecurity/Zeek-Intelligence-Feeds/refs/heads/master/compromised-ips.intel"

# Fetch the .intel file
response = requests.get(intel_file_url)
lines = response.text.splitlines()

# Remove the header (first line)
lines = lines[1:]

# Convert to CSV and save
csv_file_path = "output.csv"
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    for line in lines:
        # Split the line by tabs (assuming the .intel file is tab-separated)
        csv_writer.writerow(line.split('\t'))

print(f"Converted {intel_file_url} to {csv_file_path}")