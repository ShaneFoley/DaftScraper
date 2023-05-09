# Author Shane 2023
# Imports for Daft.ie WebScraper
import requests
import math
import time
from bs4 import BeautifulSoup


def get_prices(url):
    response = requests.get(url)
    # Get HTML content from first the URL page
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_element = soup.find('h1', {'data-testid': 'search-h1'})

    if h1_element:
        number = h1_element.text.split()[0]
        print("Number of Apartments found on Daft.ie: " + number)
    else:
        print("Number of Apartments could not be found on Daft.ie")

    pages = math.ceil(int(number) / 20)  # set the number of pages for the loop

    house_prices = []
    properties_per_page = 20

    for page in range(pages):
        offset = properties_per_page * page
        url = url.split('&from=')[0] + f'&from={offset}'
        response = requests.get(url)
        page_content = response.content
        soup = BeautifulSoup(page_content, "html.parser")

        # Scrape the price from the web page
        price_divs = soup.find_all("div", attrs={"data-testid": "price"})

        for div in price_divs:
            price = div.h3.text.strip()
            if price.startswith('€'):
                price = price.replace(',', '').replace('€', '')
                price = int(price)
                house_prices.append(price)

    #time.sleep(2)  # Add a 2-second delay between requests, make requests appear normal

    average = round(sum(house_prices) / len(house_prices))  # Calculate the average
    print(f"Average price: €{average}")  # Print result


# Load in Daft URLs & Print the Prices obtained.
print("-----------------------------------------------------")
print("One Bedroom Apartments 3km Radius Clonskeagh")
oneBedApartments = "https://www.daft.ie/property-for-sale/clonskeagh-dublin/apartments?radius=3000&" \
                   "pageSize=20&numBeds_from=1&numBeds_to=1"
get_prices(oneBedApartments)

print("-----------------------------------------------------")

print("Two Bedroom Apartments 3km Radius Clonskeagh")
twoBedApartments = "https://www.daft.ie/property-for-sale/clonskeagh-dublin/apartments?radius=3000" \
                   "&pageSize=20&numBeds_from=2&numBeds_to=2"
get_prices(twoBedApartments)
