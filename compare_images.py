from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
import imagehash
import sys

client = ScrapingBeeClient(api_key='UO8H6A67OVIPPBNGT233G2LIV20OA3MK5F1WXNHAQVBRVB98733LP55HILQZJIU0J8OF5GE7CYTJQA1B')

url = input("Enter the URL you want to scrape: ")
ref_image_path = input("Enter the path to the reference image file: ")

response = client.get(url)

if response.status_code == 200:
    content_str = response.content.decode('utf-8')

    soup = BeautifulSoup(content_str, 'html.parser')

    img_tags = soup.find_all('img')

    ref_img = Image.open(ref_image_path)

    ref_hash = imagehash.average_hash(ref_img)

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        print(f'Image URL found: {img_url}')

        if img_url:
            try:
                img_response = requests.get(img_url)
                img = Image.open(BytesIO(img_response.content))

                img_hash = imagehash.average_hash(img)

                if img_hash == ref_hash:
                    print("Match found! Stopping script.")
                    sys.exit(0)

            except Exception as e:
                print(f'Error downloading or comparing image: {e}')

else:
    print(f'Failed to retrieve the webpage. ScrapingBee error: {response.status_code}')

print("No match found.")
