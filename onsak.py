import requests
from bs4 import BeautifulSoup
import os
import shutil

# خواندن لینک‌ها از سکرت گیتهاب
raw_urls = os.getenv("TARGET_URLS", "")
URLS = [url.strip() for url in raw_urls.split(",") if url.strip()]

def scrape():
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.makedirs('output')

    for i, url in enumerate(URLS):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=20, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for s in soup(["script", "style"]):
                s.extract()
            
            text = soup.get_text(separator='\n')
            clean_text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

            # ذخیره با پسوند ظاهری .data
            with open(f"output/data_{i+1}.data", "w", encoding="utf-8") as f:
                f.write(clean_text)
            print(f"Done: {url}")
        except Exception as e:
            print(f"Error {url}: {e}")

if __name__ == "__main__":
    scrape()
