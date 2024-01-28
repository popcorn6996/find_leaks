from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
import imagehash
import sys

# Replace 'your_api_key' with your actual ScrapingBee API key
client = ScrapingBeeClient(api_key='UO8H6A67OVIPPBNGT233G2LIV20OA3MK5F1WXNHAQVBRVB98733LP55HILQZJIU0J8OF5GE7CYTJQA1B')

# User input for the URL and the path to the reference image
url = input("Enter the URL you want to scrape: ")
ref_image_path = input("Enter the path to the reference image file: ")

# Make a request to ScrapingBee to get the HTML content
response = client.get(url)

# Check if the request to ScrapingBee was successful
if response.status_code == 200:
    # Decode the response content to convert it to a string
    content_str = response.content.decode('utf-8')

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(content_str, 'html.parser')

    # Find all image tags in the HTML
    img_tags = soup.find_all('img')

    # Load the reference image
    ref_img = Image.open(ref_image_path)

    # Calculate hash for the reference image
    ref_hash = imagehash.average_hash(ref_img)

    # Extract and compare image URLs
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        print(f'Image URL found: {img_url}')

        # Optionally, download and compare the image
        if img_url:
            try:
                # Download the image
                img_response = requests.get(img_url)
                img = Image.open(BytesIO(img_response.content))

                # Calculate hash for the current image
                img_hash = imagehash.average_hash(img)

                # Compare the hash values
                if img_hash == ref_hash:
                    print("Match found! Stopping script.")
                    sys.exit(0)

            except Exception as e:
                print(f'Error downloading or comparing image: {e}')

else:
    print(f'Failed to retrieve the webpage. ScrapingBee error: {response.status_code}')

print("No match found.")
