import os
from scrapper.config import START_URLS, OUTPUT_DIR
from scrapper.crawler import crawl, fetch_html
from scrapper.parser import parse_product_page
from scrapper.downloader import download_zip, extract_and_save_step
from scrapper.utils import normalize_segment, ensure_dir

def main():
    print("Starting crawler...")

    all_urls = crawl(START_URLS)
    print(f"Total URLs found: {len(all_urls)}")

    for url in all_urls:
        try:
            html = fetch_html(url)
        except Exception as e:
            print(f"Failed to fetch page {url}: {e}")
            continue

        # Extract breadcrumbs and STEP URL
        crumbs, step_url = parse_product_page(html)
        if not crumbs or not step_url:
            continue  # Not a product page with STEP file

        # Normalize breadcrumbs for folder path
        path_segments = [normalize_segment(x) for x in crumbs]
        save_dir = os.path.join(OUTPUT_DIR, *path_segments)

        # Part name from ZIP URL
        part_name = os.path.basename(step_url).replace(".zip", "")

        # Download ZIP and extract STEP
        try:
            zip_bytes = download_zip(step_url)
            extract_and_save_step(zip_bytes, save_dir, part_name)
        except Exception as e:
            print(f"FAILED {url} -> {e}")

if __name__ == "__main__":
    main()