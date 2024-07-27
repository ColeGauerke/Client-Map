import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import re
import time

#Loading in and Reading the Spreadsheet
file_path = 'Full_Address_Company_List.csv'
data = pd.read_csv(file_path)
total_rows = len(data)
start_time = time.time()

#This is the pattern that the address wil be set to match
address_pattern = re.compile(r'^\d+\s+[\w\s]+,\s+\w+,\s+[A-Z]{2}\s+\d{5}')

#function to determine if the address is valid
def is_valid_address(address):
    if pd.isna(address):
        return False
    address = str(address)
    address_pattern = re.compile(r'^\d+\s+[\w\s]+,\s+\w+,\s+[A-Z]{2}\s+\d{5}')
    return bool(address_pattern.match(address))

#Function to find the address given the company name and using search results
def get_address_from_company_name(company_name):
    geolocator = Nominatim(user_agent="address_validator")
    try:
        location = geolocator.geocode(company_name)
        if location:
            return f"{location.address}"
        else:
            return None
    except GeocoderTimedOut:
        return None
    
#Sort through the rows and check the address 
for index, row in data.iterrows():
    if not is_valid_address(row['full_address']):
        new_address = get_address_from_company_name(row['name'])
        if new_address:
            data.at[index, 'full_address'] = new_address
    
    if (index + 1) % 10 == 0 or index + 1 == total_rows:
        elapsed_time = time.time() - start_time
        print(f"Processed {index + 1}/{total_rows} rows in {elapsed_time:.2f} seconds")

#Saving the updated spreadsheet as an Excel File
updated_file_path = 'client_list.xlsx'
data.to_excel(updated_file_path,index = False)
print(f"Updated addresses saved to {updated_file_path}")
