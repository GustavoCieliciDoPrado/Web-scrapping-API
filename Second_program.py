from urllib import response
from bs4 import BeautifulSoup
import requests
from pprint import pprint

# Amend the URL to the actual page you want to scrape by changing the postcode
url = 'https://landregistry.data.gov.uk/app/ppd/search?et%5B%5D=lrcommon%3Afreehold&et%5B%5D=lrcommon%3Aleasehold&limit=1000&nb%5B%5D=true&nb%5B%5D=false&postcode=UB6&ptype%5B%5D=lrcommon%3Adetached&ptype%5B%5D=lrcommon%3Asemi-detached&ptype%5B%5D=lrcommon%3Aterraced&ptype%5B%5D=lrcommon%3Aflat-maisonette&ptype%5B%5D=lrcommon%3AotherPropertyType&relative_url_root=%2Fapp%2Fppd&tc%5B%5D=ppd%3AstandardPricePaidTransaction&tc%5B%5D=ppd%3AadditionalPricePaidTransaction'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

properties = soup.select('ul.ppd-results > li')
results = []
for prop in properties:
    record = {}

    # The poroperty Adress as the Title
    title = prop.select_one('h3')
    record['property_address'] = title.get_text(strip=True) if title else None

    # Transaction History, including the date of the transaction and the price paid
    transactions = []
    rows = prop.select('.transaction-history tbody tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue

        transaction = {
            'transaction_date': cells[1].get_text(strip=True),
            'price_paid': int(cells[2].get_text(strip=True).replace('£', '').replace(',', ''))
        }
        transactions.append(transaction)

    record['transactions'] = transactions

    # Detailed property address, including building name, street, and postcode
    def get_detail(label):
        cell = prop.find('td', string=label)
        return cell.find_next_sibling('td').get_text(strip=True) if cell else None
    
    record['secondary_name'] = get_detail('secondary name')
    record['building_name'] = get_detail('building name or number')
    record['street'] = get_detail('street')
    record['postcode'] = get_detail('postcode')

    # The property attributes, such as the property type, tenure, and whether it is new build
    def get_attribute(label):
        cell = prop.find('td', string=label)
        return cell.find_next_sibling('td').get_text(strip=True) if cell else None
    record['property_type'] = get_attribute('property type')
    record['estate_type'] = get_attribute('estate type')
    record['new_build'] = get_attribute('new build?')

    results.append(record)
    pprint(results[0]) # Print the first record to verify the output

# The code worked and I manage to get the results by properties rather than un related, however, there are some queries that are ruturning as null
# The reason is, my search for property address and attributes are way too vague and some parts do not exactly match the code from the website I am scrapping, and finally some fields reside in a different table.
