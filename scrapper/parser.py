from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Optional

from .config import BASE_URL

def parse_product_page(html: str) -> tuple[Optional[str], Optional[str]]:
    """
    Extract:
    - breadcrumb path as list of normalized segments
    - step download URL (zip)
    """
    soup = BeautifulSoup(html, "html.parser")

    # Breadcrumb
    crumbs = []
    for li in soup.select("ul.breadcrumbs li"):
        a = li.find("a", class_="breadcrumb-label")
        if a and a.text:
            crumbs.append(a.text)

    # Find STEP ZIP link
    link = soup.find("a", class_="product-downloadsList-listItem-link")
    step_url = None
    if link and link.get("href"):
        step_url = urljoin(BASE_URL, link["href"])

    return crumbs, step_url