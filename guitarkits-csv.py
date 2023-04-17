import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm


def extract_feature(soup, feature):
    pattern = re.compile(f"{feature}:\\s*(.*)")
    result = soup.find(string=pattern)
    if result:
        return pattern.search(result).group(1).strip()
    else:
        return None


def extract_image(soup):
    img = soup.find("img", {"class": "photoswipe__image"})
    if img:
        img_url = img["data-photoswipe-src"]
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        return img_url
    else:
        return None


def extract_model(url):
    model = url.split("/")[-1].replace("-", " ").title()
    return model


def extract_price(soup):
    on_sale = soup.find("span", {"class": "product__price on-sale"})
    price = soup.find("span", {"class": "product__price"})
    if on_sale:
        return on_sale.get_text(strip=True)
    elif price:
        return price.get_text().strip()
    else:
        return None


def get_info():
    csv_name = "guitarKit.csv"
    url = "https://www.guitarkit.shop/en-ca/collections/guitar-kit"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    last_page = pagination.find_all("a")[-2].text if pagination else 1

    product_info = []
    for page in tqdm(range(1, int(last_page) + 1)):
        url = f"https://www.guitarkit.shop/en-ca/collections/guitar-kit?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        page_links = soup.find_all("a", {"class": "grid-product__link"})
        for link in tqdm(page_links):
            product_url = "https://www.guitarkit.shop" + link.get("href")
            response = requests.get(product_url)
            soup = BeautifulSoup(response.text, "html.parser")
            description = soup.find("div", {"class": "product-single__description"})
            row = {
                "URL": product_url,
                "Image": extract_image(soup),
                "Model": extract_model(product_url),
                "Scale": extract_feature(description, "Scale")
                or extract_feature(description, "Scale length"),
                "Body": extract_feature(description, "Body"),
                "Neck": extract_feature(description, "Neck"),
                "Fingerboard": extract_feature(description, "Fingerboard"),
                "Pickup": extract_feature(description, "Pickup"),
                "Hardware": extract_feature(description, "Hardware"),
                "Orientation": extract_feature(description, "Orientation"),
                "Pickguard": extract_feature(description, "Pickguard"),
                "Price": extract_price(soup),
            }
            product_info.append(row)

    df = pd.DataFrame(product_info)
    df.to_csv(csv_name, index=False)
    print(f"CSV: {csv_name}")

    return product_info


get_info()
