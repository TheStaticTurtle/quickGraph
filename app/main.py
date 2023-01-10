from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
import re

from starlette import status
from starlette.responses import Response

app = FastAPI()

regex_url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_ip(ip):
    return ip.count('.') == 3 and  all(0<=int(num)<256 for num in ip.rstrip().split('.'))

def parse_page(page_url):
    response = requests.get(page_url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    })

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    found_tags = {}
    for meta_tag in soup.find_all("meta"):
        if meta_tag.has_attr("property") and meta_tag.has_attr("content") and (meta_tag["property"].startswith("og:") or meta_tag["property"].startswith("twitter:")):
            found_tags[meta_tag["property"]] = meta_tag["content"]
    return found_tags


@app.get("/parse")
async def root(url: str, response: Response):
    if re.match(regex_url, url) is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Invalid uri"}

    url_parsed = urlparse(url)
    if url_parsed.scheme not in ["http", "https"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"Scheme {url_parsed.scheme} is not allowed"}

    if url_parsed.netloc.startswith("localhost") or is_ip(url_parsed.netloc):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"IPs/Localhost are not allowed"}

    data = parse_page(url)
    response.status_code = status.HTTP_200_OK
    return {
        "url": url_parsed,
        "opengraph": data
    }
