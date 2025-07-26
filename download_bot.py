import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import base64
import requests

def get_direct_mediafire_link_with_browser(driver, mediafire_url):
    print(f"Navigating to Mediafire page: {mediafire_url}")
    driver.get(mediafire_url)

    try:
        download_button_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "downloadButton"))
        )

        href = download_button_element.get_attribute("href")
        if href and href.startswith("javascript"):
            scrambled_url = download_button_element.get_attribute("data-scrambled-url")
            if scrambled_url:
                decoded_url = base64.b64decode(scrambled_url).decode('utf-8')
                return decoded_url
            else:
                raise ValueError("data-scrambled-url not found, cannot extract direct link.")
        else:
            return href
    except Exception as e:
        print(f"Error finding download button or extracting URL: {e}")
        page_source = driver.page_source
        import re
        pattern = re.compile(r'https://download\d+\.mediafire\.com/[\w./\-_%]+')
        matches = pattern.findall(page_source)
        if matches:
            return matches[0]
        raise ValueError("Could not find direct download link on Mediafire page.")

def download_file_http(direct_url, output_folder='.'):
    local_filename = os.path.join(output_folder, os.path.basename(direct_url).split('?')[0])
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/91.0.4472.124 Safari/537.36")
    }
    print(f"Downloading from: {direct_url}")
    with requests.get(direct_url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"Downloaded file saved as: {local_filename}")

def read_urls_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

if __name__ == '__main__':
    input_file = 'mediafire_links.txt'  # Your text file with Mediafire URLs
    output_folder = '.'  # or any folder where you want files saved

    urls = read_urls_from_file(input_file)
    print(f"Total URLs to process: {len(urls)}")

    # Initialize undetected_chromedriver browser
    driver = uc.Chrome(headless=False)  # Set True to run headless
    
    try:
        for idx, mediafire_url in enumerate(urls, 1):
            print(f"\nProcessing [{idx}/{len(urls)}]: {mediafire_url}")
            try:
                direct_url = get_direct_mediafire_link_with_browser(driver, mediafire_url)
                print(f"Direct download URL: {direct_url}")
                download_file_http(direct_url, output_folder=output_folder)
            except Exception as e:
                print(f"Failed to process {mediafire_url}: {e}")
    finally:
        driver.quit()
        print("Browser closed.")
