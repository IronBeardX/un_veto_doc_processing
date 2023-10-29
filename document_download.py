import json
import requests
from bs4 import BeautifulSoup

# Specify the path to the downloaded HTML file
file_path = "un_veto_table_en.htm"

# Open the file in binary mode and read its contents
with open(file_path, 'rb') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Locate the table you want to scrape
table = soup.find('table')

# nitialize an empty dictionary to store the data
data_dict = {}

# Iterate through the rows of the table and extract data
for row_num, row in enumerate(table.find_all('tr'), 1):
    if row_num in (1, 2, 3, 4):
        continue
    cells = row.find_all(['td', 'th'])
    
    # Extract the data from each row
    date = cells[0].get_text(strip=True)
    identifier = cells[1].get_text(strip=True)
    document_location = cells[1].find("a").get('href')
    subject = cells[3].get_text(strip=True).replace('\n', '').replace('\t', '')
    vetoing_member = cells[4].get_text(strip=True)

    # Downloading the pdf document
    response = requests.get(document_location)
    response_2 = requests.get(response.url)
    response_3 = requests.get(response_2.url)
    response_4 = requests.get(response_3.url)
    if response.status_code == 200:
        with open(f'./Documents/{date}', 'wb') as f:
            f.write(response.content)
    else:
        print(f'Failed to download pdf:{response.status_code}')

    entry = {
        "date": date,
        "vetoing_members": [member for member in ("China", "Russia", "USA", "UK", "France", "USSR") if (member in vetoing_member)],
        "subject": subject,
        "document_name": ""
    }
    # Adding the entry to the dictionary 
    data_dict[identifier] = entry

# Write the data to a JSON file
output_file = "output.json"
with open(output_file, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f"Data has been saved to {output_file}")
