#----This was my first version of trial and error for the WSA
#----I coded this one parameter at a time so I could visualise the result and the format it would return me as

from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://landregistry.data.gov.uk/app/ppd/search?et%5B%5D=lrcommon%3Afreehold&et%5B%5D=lrcommon%3Aleasehold&limit=1000&nb%5B%5D=true&nb%5B%5D=false&postcode=UB6&ptype%5B%5D=lrcommon%3Adetached&ptype%5B%5D=lrcommon%3Asemi-detached&ptype%5B%5D=lrcommon%3Aterraced&ptype%5B%5D=lrcommon%3Aflat-maisonette&ptype%5B%5D=lrcommon%3AotherPropertyType&relative_url_root=%2Fapp%2Fppd&tc%5B%5D=ppd%3AstandardPricePaidTransaction&tc%5B%5D=ppd%3AadditionalPricePaidTransaction').text
soup = BeautifulSoup(html_text, 'lxml')
p_adds = soup.find_all('h2', class_ = 'property-heading col-md-12')
for p_add in p_adds:
    p_add = p_add.find('span', class_ = 'address').text
    print(p_add)
tx_values = soup.find_all('td', class_ = 'text-right')
for value in tx_values:
    value = value.text.replace('£', '').replace(',', '')
    print(value)
txdate = soup.find('table', class_ = 'table').text.split()[-2].replace('    ', '')
attribute = soup.find('div', class_ = 'col-md-4 property-characteristics')
p_att = attribute.find('tbody').text.replace('\n', ' ').strip()
print(p_att)
print(txdate)

#----What I learnt from this attempt was, this would return the information I needed, however it would break it up from it's parent data. In other words, I had the data but did not know which data belonged together.
#----I had to extract the data as a whole unit rather than one value at a time.
