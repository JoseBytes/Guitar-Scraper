import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def extract_desc(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    
    info = {}
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            info[key] = value

    return info

def get_num_page():
    url = "https://combineguitars.com/collections/diy-guitar-kits"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.find(class_="pagination__text").get_text()
    num_pages = page_text.split()[-1]
    return int(num_pages)

def get_url():
    num_pages = get_num_page()
    result_urls = []
    base_url = "https://combineguitars.com/collections/diy-guitar-kits?page={}"
    for page in tqdm(range(1, num_pages + 1)):
        url = base_url.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select(".grid-view-item__link"):
            href = link.get("href")
            if href.startswith("/products/"):
                full_url = "https://combineguitars.com" + href
                result_urls.append(full_url)
    return result_urls

def get_title(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('h1', {'class': 'product-single__title'}).text
    return title

def get_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find(class_="price-item--regular").get_text().strip()
    return price

def get_img(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    zoom_wrapper = soup.find('div', {'class': 'product-single__media'})
    if zoom_wrapper:
        img_url = zoom_wrapper['data-zoom']
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        return img_url
    return None

def get_info():
    csv_name = 'combineguitars.csv'
    data = []
    urls = get_url()
    for url in tqdm(urls):
        title = get_title(url)
        img_url = get_img(url)
        price = get_price(url)
        description = extract_desc(url)

        if description is not None:
            row = {
                'URL': url,
                'Image': img_url,
                'Title': title,
                'Body Material': description.get('Body Material', ''),
                'Neck Material': description.get('Neck Material', ''),
                'Fingerboard Material': description.get('Fingerboard Material', ''),
                'Scale Length': description.get('Scale Length', ''),
                'Fret Count': description.get('Fret Count', ''),
                'Control': description.get('Control', ''),
                'Pickups': description.get('Pickups', ''),
                'Bridge': description.get('Bridge', ''),
                'Hardware': description.get('Hardware', ''),
                'Joint': description.get('Joint', ''),
                'Hand Orientation': description.get('Hand Orientation', ''),
                'Truss Rod': description.get('Truss Rod', ''),
                'Price': price,
            }

            data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(csv_name, index=False)
    print(f"CSV: {csv_name}")
    return data

get_info()
