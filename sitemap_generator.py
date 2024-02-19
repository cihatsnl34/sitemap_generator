import requests
from bs4 import BeautifulSoup
import pandas as pd

# Your website's main URL
base_url = 'https://www.example.com'
urls = set([base_url])  # Create a set containing the homepage initially
checked_urls = set()  # A set to keep track of already checked URLs

# Function to collect URLs
def scrape_urls(current_url):
    global urls, checked_urls
    if current_url not in checked_urls and current_url.startswith(base_url):
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = base_url + href
                if href.startswith(base_url):
                    urls.add(href)
                    
            checked_urls.add(current_url)
        except Exception as e:
            print(f"Hata: {e}")

# Collect all URLs starting from the main URL
while urls - checked_urls:
    for url in list(urls - checked_urls):
        scrape_urls(url)

# Convert collected URLs into a DataFrame
df = pd.DataFrame(list(urls), columns=['URL'])

# Save DataFrame to Excel file
excel_filename = 'sitemap.xlsx'
df.to_excel(excel_filename, index=False)
print(f'Sitemap saved as {excel_filename}.')