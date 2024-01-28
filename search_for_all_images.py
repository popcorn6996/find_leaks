from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image

# Replace 'your_api_key' with your actual ScrapingBee API key
client = ScrapingBeeClient(api_key='UO8H6A67OVIPPBNGT233G2LIV20OA3MK5F1WXNHAQVBRVB98733LP55HILQZJIU0J8OF5GE7CYTJQA1B')

# User input for the URLs (comma-separated)
url_input = input("Enter the URLs you want to scrape (comma-separated): ")
urls = [url.strip() for url in url_input.split(',')]

# User input for the terms to find
search_terms_input = input("Enter the terms you want to find (comma-separated): ")
search_terms = [term.strip() for term in search_terms_input.split(',')]

# Loop through each URL
for url in urls:
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

        # Extract and display image URLs
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            print(f'Image URL found: {img_url}')

            # Optionally, download and display the image
            if img_url:
                try:
                    # Download the image
                    img_response = requests.get(img_url)
                    img = Image.open(BytesIO(img_response.content))

                    # Display the image (this might not work well in certain environments)
                    img.show()

                except Exception as e:
                    print(f'Error downloading or displaying image: {e}')

    else:
        print(f'Failed to retrieve the webpage. ScrapingBee error: {response.status_code}')
