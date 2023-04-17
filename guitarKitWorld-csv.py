import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm


def get_num_pages():
    url_base = "https://guitarkitworld.com/collections/all"
    response = requests.get(url_base)
    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.find("ul", {"class": "pagination--inner"})
    last_page = int(pagination.find_all("a")[-2].text) if pagination else 1
    return last_page


def get_url():
    url_main = "https://guitarkitworld.com"
    data = []
    num_pages = get_num_pages()
    for i in tqdm(range(1, num_pages + 1)):
        url = f"{url_main}/collections/all?page={i}&grid_list=grid-view"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        product_items = soup.find_all("h2", {"class": "productitem--title"})
        for item in product_items:
            link = item.find("a")
            if link:
                product_url = f"{url_main}{link['href']}"
            else:
                "N/A"
            data.append(product_url)
    return data


def extract_feature(soup, label):
    tag = soup.find(lambda tag: tag.name == "li" and label in tag.text)
    if tag and tag.strong:
        return tag.strong.text.strip() if tag.strong else None
    else:
        return None


def get_info():
    csv_name = "guitarKitWorld.csv"
    data = []
    product_urls = get_url()

    for url in tqdm(product_urls):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1", {"class": "product-title"}).text.strip()

        img_div = soup.find("div", {"class": "product-gallery--image-background"})
        if img_div:
            img_url = img_div.find("img")["src"]
            if img_url.startswith("//"):
                img_url = f"https:{img_url}"
        else:
            img_url = "N/A"

        price_div = soup.find("div", {"class": "price__current"})
        if price_div:
            price = price_div.find("span", {"class": "money"}).text.strip()
        else:
            price = "N/A"

        row = {
            "URL": url,
            "Image URL": img_url,
            "Title": title,
            "Hand Orientation": extract_feature(soup, "Hand Orientation"),
            "Neck Joint": extract_feature(soup, "Neck Joint"),
            "Neck Material": extract_feature(soup, "Neck Material"),
            "Neck Nut Material": extract_feature(soup, "Neck Nut Material"),
            "Fretboard Material": extract_feature(soup, "Fretboard Material"),
            "Number of Frets": extract_feature(soup, "Number of Frets"),
            "Scale Length": extract_feature(soup, "Scale Length"),
            "Body Type": extract_feature(soup, "Body type"),
            "Body Material": extract_feature(soup, "Body Material"),
            "Pickups": extract_feature(soup, "Pickups"),
            "Pickguard": extract_feature(soup, "Pickguard"),
            "Hardware Set Finish": extract_feature(soup, "Hardware Set Finish"),
            "Price": price
        }

        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(csv_name, index=False)
    print(f"CSV: {csv_name}")

    return data


get_info()
