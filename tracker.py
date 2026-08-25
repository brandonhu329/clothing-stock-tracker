import requests
from bs4 import BeautifulSoup

url = "https://www.hollisterco.com/shop/us/p/relaxed-everyday-tee-62788823?seq=33"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print(response.status_code)