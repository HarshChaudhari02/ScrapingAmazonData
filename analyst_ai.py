# import csv
# import requests
# from bs4 import BeautifulSoup
#
# # Function to scrape product details from a given URL
# def scrape_product_details(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Scrape the required information
#     product_url = url
#     product_name = soup.find('span', {'id': 'productTitle'}).text.strip()
#     product_price = soup.find('span', {'class': 'a-offscreen'}).text.strip()
#     rating = soup.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
#     reviews = soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip().split()[0]
#     description = soup.find('div', {'id': 'productDescription'}).text.strip()
#     asin = soup.find('th', text='ASIN').find_next_sibling('td').text.strip()
#
#     # Prepare the data as a dictionary
#     product_data = {
#         'Product URL': product_url,
#         'Product Name': product_name,
#         'Product Price': product_price,
#         'Rating': rating,
#         'Number of Reviews': reviews,
#         'Description': description,
#         'ASIN': asin
#     }
#
#     return product_data
#
#
# # Scrape product details from multiple pages
# base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
#
# # Create a CSV file to store the data
# csv_filename = 'product_data.csv'
# csv_file = open(csv_filename, 'w', newline='')
# csv_writer = csv.DictWriter(csv_file, fieldnames=['Product URL', 'Product Name', 'Product Price', 'Rating',
#                                                  'Number of Reviews', 'Description', 'ASIN'])
# csv_writer.writeheader()
#
# for page in range(1, 21):  # Scrape 20 pages
#     url = base_url.format(page)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     products = soup.find_all('div', {'data-component-type': 's-search-result'})
#
#     for product in products:
#         product_url = product.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
#         product_data = scrape_product_details(product_url)
#
#         # Write the product data to the CSV file
#         csv_writer.writerow(product_data)
#
# csv_file.close()

import csv
import requests
from bs4 import BeautifulSoup

def scrap_product_details(url):
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')
	product_url = url
	product_name = soup.find_all('span',{'class': 'a-size-large product-title-word-break'})
	try:
		product_name = product_name[0].text.strip()
	except:
		product_name = ''

	product_price = soup.find_all('span', {'class': 'a-price-whole'})
	product_price = product_price[0].text

	product_rating = soup.find_all('span', {'class': 'a-size-base a-color-base'})
	product_rating = product_rating[1].text

	product_reviews = soup.find_all('span', {'id': 'acrCustomerReviewText'})
	product_reviews = product_reviews[0].text

	description = soup.find_all('ul', {'class': 'a-unordered-list a-vertical a-spacing-mini'})
	description = description[0].text.strip()

	head = soup.find_all('th', {'class': 'a-color-secondary a-size-base prodDetSectionEntry'})
	value = soup.find_all('td', {'class': 'a-size-base prodDetAttrValue'})

	asin = None
	manf = None
	for i in range(0, len(head)):
		data = head[i].text.strip()
		if data == 'ASIN':
			asin = value[i].text.strip()
		if data == 'Manufacturer':
			manf = value[i].text.strip()
			manf = manf.replace('\u200e', '')

	# Prepare the data as a dictionary
	product_data = {
	    'Product URL': product_url,
	    'Product Name': product_name,
	    'Product Price': product_price,
	    'Rating': product_rating,
	    'Number of Reviews': product_reviews,
	    'Description': description,
	    'ASIN': asin,
		'Manufacturer': manf
	    }

	return product_data

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

headers = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

# Create a CSV file to store the data
csv_filename = 'product_data.csv'
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.DictWriter(csv_file, fieldnames=['Product URL', 'Product Name', 'Product Price', 'Rating',
                                                 'Number of Reviews', 'Description', 'ASIN', 'Manufacturer'])
csv_writer.writeheader()


for page in range(1,21):
	url = base_url.format(page)
	print(url)
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')

	products = soup.find_all('h2',{'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
	for product in products:
		product = product.a.attrs['href']
		# Replace the URL format
		modified_url = product.split('url=')
		try:
			modified_url = modified_url[1]
			modified_url = modified_url.replace("%2F", "/")
			modified_url = modified_url.replace("%3D", "=")
			modified_url = modified_url.replace("%26", "&")
		except:
			pass

		if modified_url[0] != '/':
			modified_url = modified_url[0]
			modified_url = 'https://www.amazon.in' + modified_url
			print(modified_url)
			product_data = scrap_product_details(modified_url)
			# Write the product data to the CSV file
			csv_writer.writerow(product_data)

csv_file.close()