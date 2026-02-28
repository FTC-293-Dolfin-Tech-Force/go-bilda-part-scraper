import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Set
from .config import BASE_URL

# Skip binary/content files we can't parse
SKIP_EXTENSIONS = (
    ".zip", ".step", ".stp", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg"
)

def fetch_html(url: str) -> str:
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def find_links(html: str, base: str) -> Set[str]:
    """
    Parse HTML and find internal links to follow.
    Skip binary content like ZIPs/images.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"Error parsing HTML from {base}: {e}")
        return set()

    urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]

        # skip external
        if href.startswith("http") and BASE_URL not in href:
            continue

        full = urljoin(base, href)

        # skip non-HTML files
        if full.lower().endswith(SKIP_EXTENSIONS):
            continue

        if BASE_URL in full:
            urls.add(full)

    return urls

def crawl(start_urls: list[str]) -> Set[str]:
    """
    BFS crawl starting from top-level category URLs.
    Only collects HTML pages.
    """
    visited = set()
    to_visit = set(start_urls)

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue

        print(f"Crawling: {url}")
        visited.add(url)

        try:
            html = fetch_html(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        try:
            links = find_links(html, url)
        except Exception as e:
            print(f"Skipping {url}: not HTML ({e})")
            continue

        for link in links:
            if link not in visited:
                to_visit.add(link)

    return visited