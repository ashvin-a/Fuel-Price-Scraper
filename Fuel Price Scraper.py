import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv

url = " https://www.newsrain.in/petrol-diesel-prices"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

articles = soup.find_all('article')

place = []
petrolPrice = []
dieselPrice = []

for article in articles:
    state = article.find("div", class_='fuel-title')
    city = state.find("small",class_='center')
    placeName = state.contents[0].strip() + "-" +city.contents[0].strip()
    place.append(placeName)
    fuelcontent = article.find("div",class_="fuel-content")
    products = fuelcontent.find_all("div",{"itemprop": "product"})
    for product in products:
        productName = product.find("h3",{"itemprop":"name"}).contents[0].strip()
        productPrice = product.find("span",class_="price_tag").contents[0].strip()
        productCurrency = product.find("i",{"itemprop":"priceCurrency"})["content"]
        priceChange = product.find("span",class_="changed-price").contents[0].strip()

        increment = product.find("span",class_="increment")
        if increment == None:
            priceChangeSign = "+"
        else:
            priceChangeSign = "-"
        if productName == "Petrol":
            petrolPrice.append(productPrice)
        else:
            dieselPrice.append(productPrice)

columnName = ["Place", "Petrol_Price", "Diesel_Price"]
df = pd.DataFrame([place, petrolPrice, dieselPrice], index=columnName)
df = df.T
df.to_csv('fuelprice.csv')

graph = pd.read_csv("./fuelprice.csv")
plt.title('Petrol - Diesel Price in India')
plt.barh(graph['Place'], graph['Petrol_Price'], color = 'b',label = "Petrol")
plt.barh(graph['Place'], graph['Diesel_Price'], color = 'g',label = "Diesel")

plt.xlabel("Fuel Price")
plt.ylabel("Place")
plt.legend()
plt.show()
