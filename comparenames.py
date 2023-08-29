import csv

# Read the original CSV file containing data
def read_original_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

original_data = read_original_data('170USList.csv')

# Read the CSV file containing names for comparison
def read_comparison_names(file_path, first_name_column, last_name_column):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row[first_name_column].lower(), row[last_name_column].lower()) for row in reader]

comparison_names = read_comparison_names('schedule_a-2023-08-25T09_32_02.csv', 'contributor_first_name', 'contributor_last_name')

# Read the donation data from the second CSV file
def read_donation_data(file_path, first_name_column, last_name_column, donation_column):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        donation_data = {}
        for row in reader:
            first_name = row[first_name_column].lower()
            last_name = row[last_name_column].lower()
            donation_data[(first_name, last_name)] = row[donation_column]
        return donation_data

donation_data = read_donation_data('schedule_a-2023-08-25T09_32_02.csv', 'contributor_first_name', 'contributor_last_name', 'contributor_aggregate_ytd')

# Create a new list of records with added columns
new_data = []
for row in original_data:
    first_name = row['FirstName'].lower()
    last_name = row['LastName'].lower()
    donor = "Found" if (first_name, last_name) in comparison_names else "Not Found"
    donation = donation_data.get((first_name, last_name), 'NA')
    new_row = dict(row)
    new_row['Donor'] = donor
    new_row['Donations$'] = donation
    new_data.append(new_row)

# Write the new data to the new CSV file
fieldnames = list(original_data[0].keys()) + ['Donor', 'Donations$']
with open('170USListCMP.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_data)

print("CSV file '170USListCMP.csv' created successfully.")

