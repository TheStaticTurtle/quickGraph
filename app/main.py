from urllib.parse import urlparse

from fastapi import FastAPI
from opengraph_parse import parse_page
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
