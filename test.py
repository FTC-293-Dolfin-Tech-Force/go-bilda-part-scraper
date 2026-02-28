from scrapper.crawler import fetch_html
from scrapper.parser import parse_product_page

from scrapper.downloader import download_zip, extract_and_save_step
from scrapper.utils import normalize_segment, ensure_dir
import os

test_url = "https://www.gobilda.com/1102-series-flat-beam-3-hole-24mm-length-2-pack/"
html = fetch_html(test_url)
crumbs, step_url = parse_product_page(html)
print("Breadcrumbs:", crumbs)
print("STEP URL:", step_url)

path_segments = [normalize_segment(x) for x in crumbs]
save_dir = os.path.join("parts", *path_segments)

# download and extract
zip_bytes = download_zip(step_url)
extract_and_save_step(zip_bytes, save_dir, "1102-0003-0024")