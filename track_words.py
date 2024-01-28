from scrapingbee import ScrapingBeeClient

# Replace 'your_api_key' with your actual ScrapingBee API key
SCRAPINGBEE_API_KEY = 'UO8H6A67OVIPPBNGT233G2LIV20OA3MK5F1WXNHAQVBRVB98733LP55HILQZJIU0J8OF5GE7CYTJQA1B'
client = ScrapingBeeClient(api_key=SCRAPINGBEE_API_KEY)

def scrape_url(url, search_terms):
    try:
        # Make a request to ScrapingBee to get the HTML content
        response = client.get(url)

        # Check if the request to ScrapingBee was successful
        if response.status_code == 200:
            # Decode the response content to convert it to a string
            content_str = response.content.decode('utf-8')

            # Filter and check for specific words in the response content
            matches = {term: term in content_str for term in search_terms}

            return {'status': 'success', 'matches': matches}

        return {'status': 'error', 'message': f'Failed to retrieve the webpage. ScrapingBee error: {response.status_code}'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    url = input("Enter the URL: ")
    search_terms = [term.strip() for term in input("Enter search terms (comma-separated): ").split(',')]

    result = scrape_url(url, search_terms)
    print(result)
