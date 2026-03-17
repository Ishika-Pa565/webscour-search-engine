import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ----------------------------
# Fetch Page (with headers)
# ----------------------------
def fetch_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        print("Error fetching:", url)
        print("Reason:", e)
        return None


# ----------------------------
# Extract Links
# ----------------------------
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, tag["href"])

        if absolute_url.startswith("http"):
            links.add(absolute_url)

    return links


# ----------------------------
# Crawler
# ----------------------------
def crawler(seed_url, max_pages=5):
    QUEUE = [seed_url]
    VISITED = set()

    page_count = 0

    while QUEUE and page_count < max_pages:
        current_url = QUEUE.pop(0)

        if current_url in VISITED:
            continue

        print(f"\nFetching: {current_url}")

        html = fetch_page(current_url)

        if html is None:
            continue

        VISITED.add(current_url)
        page_count += 1

        # ✅ FIXED SAVE LOCATION
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(BASE_DIR, "pages")
        os.makedirs(folder_path, exist_ok=True)

        filename = f"page_{page_count}.html"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        print("Saved at:", file_path)

        links = extract_links(html, current_url)
        print(f"Extracted {len(links)} links")

        for link in links:
            if link not in VISITED:
                QUEUE.append(link)

    print("\nCrawling Completed!")
    print("Total pages crawled:", page_count)


# ----------------------------
# START
# ----------------------------
seed_url = "https://timesofindia.indiatimes.com/"
crawler(seed_url, max_pages=5)
