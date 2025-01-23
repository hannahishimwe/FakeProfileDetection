"""https://github.com/tizfa/tweepfake_deepfake_text_detection 
where I got my datasets from"""


import csv


def parse_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter=';')  # Using ';' as the delimiter
        writer = csv.writer(outfile)
        
        # Writing the header row
        writer.writerow(["screen_name", "text", "account.type", "class_type"])
        
        for row in reader:
            # Ensure each row has exactly 4 columns by filling missing ones if necessary
            while len(row) < 4:
                row.append('')  # Add empty string if there are missing fields
            writer.writerow(row[:4])  # Only take the first 4 columns to avoid extra data

# Example usage
input_csv = "input.csv"  # Replace with your input file path
output_csv = "output.csv"   # Output file path
parse_csv(input_csv, output_csv)
print(f"Structured CSV saved as {output_csv}")


