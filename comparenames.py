import csv

def read_original_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def read_comparison_names(file_path, first_name_column, last_name_column):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row[first_name_column].lower(), row[last_name_column].lower()) for row in reader]

def read_donation_data(file_path, first_name_column, last_name_column, donation_column):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        donation_data = {}
        for row in reader:
            first_name = row[first_name_column].lower()
            last_name = row[last_name_column].lower()
            name_key = (first_name, last_name)
            if name_key not in donation_data:
                donation_data[name_key] = []
            donation_data[name_key].append(row[donation_column])
        return donation_data

def create_final_data():
    print("Reading original data...")
    original_data = read_original_data('15kNames.csv')
    
    print("Reading and comparing data for 2023...")
    comparison_names_2023 = read_comparison_names('schedule_a-2023-08-25T09_32_02.csv', 'contributor_first_name', 'contributor_last_name')
    donation_data_2023 = read_donation_data('schedule_a-2023-08-25T09_32_02.csv', 'contributor_first_name', 'contributor_last_name', 'contribution_receipt_amount')
    
    print("Reading and comparing data for 2022...")
    comparison_names_2022 = read_comparison_names('schedule_a-2023-08-29T11_50_12.csv', 'contributor_first_name', 'contributor_last_name')
    donation_data_2022 = read_donation_data('schedule_a-2023-08-29T11_50_12.csv', 'contributor_first_name', 'contributor_last_name', 'contribution_receipt_amount')
    
    final_data = []
    for row in original_data:
        first_name = row['firstName'].lower()
        last_name = row['lastName'].lower()
        donor_2023 = "" if (first_name, last_name) not in comparison_names_2023 else "Found"

        donations_2023_dict = {}
        for donation_amount in donation_data_2023.get((first_name, last_name), ['0.00']):
            if donation_amount not in donations_2023_dict:
                donations_2023_dict[donation_amount] = 1
            else:
                donations_2023_dict[donation_amount] += 1
        donations_2023 = '; '.join(f"{amount}({count})" for amount, count in donations_2023_dict.items())
        
        donor_2022 = "" if (first_name, last_name) not in comparison_names_2022 else "Found"

        donations_2022_dict = {}
        for donation_amount in donation_data_2022.get((first_name, last_name), ['0.00']):
            if donation_amount not in donations_2022_dict:
                donations_2022_dict[donation_amount] = 1
            else:
                donations_2022_dict[donation_amount] += 1
        donations_2022 = '; '.join(f"{amount}({count})" for amount, count in donations_2022_dict.items())
        
        matches_2023 = sum(1 for name in comparison_names_2023 if (first_name, last_name) == name)
        matches_2022 = sum(1 for name in comparison_names_2022 if (first_name, last_name) == name)
        
        final_data.append({
            'firstName': row['firstName'],
            'lastName': row['lastName'],
            '23Donor': donor_2023,
            '23Donations$': donations_2023,
            '2023matches#': matches_2023,
            '2023TOTAL#': '',
            '22Donor': donor_2022,
            '22Donations$': donations_2022,
            '2022matches#': matches_2022,
            '2022TOTAL#': '',
        })
        
    return final_data

def write_to_csv(data):
    fieldnames = ['firstName', 'lastName', '23Donor', '23Donations$', '2023matches#', '2023TOTAL#', '22Donor', '22Donations$', '2022matches#', '2022TOTAL#']
    with open('15kNamesCMP.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

print("Starting the process...")
final_data = create_final_data()

total_2023_matches = sum(1 for row in final_data if row['23Donor'] == 'Found')
total_2022_matches = sum(1 for row in final_data if row['22Donor'] == 'Found')
for row in final_data:
    row['2023TOTAL#'] = total_2023_matches
    row['2022TOTAL#'] = total_2022_matches

write_to_csv(final_data)
print("Process completed.")
