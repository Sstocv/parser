from bs4 import BeautifulSoup
import requests
import os
import json


url = input("Введите ссылку на сайт - ")
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.848 Yowser/2.5 Safari/537.36"
}
url_link = "https://www.citilink.ru"


req = requests.get(url, headers=headers)
src = req.text


if not os.path.isdir("data"):
    os.mkdir("data")

# with open("index.html", "w", encoding="utf-8-sig") as file:
#     file.write(src)


# with open("index.html", encoding="utf-8-sig") as file:
#     src = file.read()


soup = BeautifulSoup(src, "lxml")


oneBlock = soup.find("div", class_="ProductCardCategoryList__list")
twoBlock = soup.find_all("div", class_="ProductCardCategoryList__grid")


cardItem = []
href = []
if oneBlock:
    itemInfoList = soup.find_all("div", class_="product_data__gtm-js")
    for item in itemInfoList:
        webName = soup.find("h1", class_="Heading Heading_level_1 Subcategory__title js--Subcategory__title").get_text(strip=True)
        cardItem.append(
            {
                "title": item.find("a", class_="ProductCardHorizontal__title").get_text(strip=True),
                "price": item.find("span", class_="ProductCardHorizontal__price_current-price").get_text(strip=True) + " руб.",
                "href": url_link + item.find("a", class_="ProductCardHorizontal__title").get("href")
            }
        )
        href.append(
            {
                "href": url_link + item.find("a", class_="ProductCardHorizontal__title").get("href")
            }
        )
elif twoBlock:
    itemInfoListGrid = soup.find_all("div", class_="product_data__gtm-js")
    for item in itemInfoListGrid:
        webName = soup.find("h1", class_="Heading Heading_level_1 Subcategory__title js--Subcategory__title").get_text(strip=True)
        cardItem.append(
            {
                "title": item.find("a", class_="ProductCardVertical__name").get_text(strip=True),
                "price": item.find("span", class_="ProductCardVerticalPrice__price-current_current-price").get_text(strip=True) + " руб.",
                "href": url_link + item.find("a", class_="ProductCardVertical__name").get("href")
            }
        )
        href.append(
            {
                "href": url_link + item.find("a", class_="ProductCardHorizontal__title").get("href")
            }
        )
else:
    print("Error")


rep = " "
if oneBlock or twoBlock:
    if rep in webName:
        webName = webName.replace(rep, "_")
    
    # os.makedirs("data/" + webName)
    if not os.path.isdir("data/" + webName):
        os.makedirs("data/" + webName)

    with open(f"data/{webName}/{webName}.json", "a", encoding="utf-8-sig") as file:
        json.dump(cardItem, file, indent=4, ensure_ascii=False)
    
    with open(f"data/{webName}/test.json", "a", encoding="utf-8-sig") as file:
        json.dump(href, file, indent=4, ensure_ascii=False)


with open(f"data/{webName}/test.json", encoding="utf-8-sig") as file:
    all_item = json.load(file)

for nameHref, itemHref in all_item.items():
    reqt = requests.get(itemHref, headers=headers)
    srct = reqt.text
    
    soupt = BeautifulSoup(srct, "lxml")
    # Парсинг страницы
    itemName = soupt.find("h1", class_="Heading Heading_level_1 ProductHeader__title").get_text(strip=True)


# os.remove("index.html")