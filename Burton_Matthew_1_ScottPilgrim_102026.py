import pandas as pd
import requests
from bs4 import BeautifulSoup

"""page = requests.get('#url goes here#') """
page = requests.get('https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html')
soup = BeautifulSoup(page.content, 'html.parser')
#week = soup.find(id='seven-day-forecast-body')
#print(week)


UPC_Code = soup.find("table", class_="table table-striped").find("th", string="UPC").find_next("td").get_text(strip=True)
Book_Title = soup.find(class_="col-sm-6 product_main").find("h1").get_text(strip=True)
Price_Excluding_Tax = soup.find("table", class_="table table-striped").find("th", string="Price (excl. tax)").find_next("td").get_text(strip=True)
Price_Including_Tax = soup.find("table", class_="table table-striped").find("th", string="Price (incl. tax)").find_next("td").get_text(strip=True)
Quantity_Available = soup.find("p", class_="instock availability").get_text(strip=True)
Product_Description = soup.find("article", class_="product_page").find_all("p")[3].get_text(strip=True)
Category = soup.find("ul", class_="breadcrumb").find_all("li")[3].get_text(strip=True)
Review_Rating = soup.find("p", class_="star-rating").get("class")[1]
Image_URL = soup.find("div", class_="item active").find("img").get("src")

"""
print("UPC code: " + UPC_Code)
print("Book title: " + Book_Title)
print("Price excluding tax: " + Price_Excluding_Tax)
print("Price including tax: " + Price_Including_Tax)
print("Quantity available: " + Quantity_Available)
print("Product description: " + Product_Description)
print("category: " + Category)
print("Review rating: " + Review_Rating)
print("Image URL: " + Image_URL)
"""

ScottPilgrim =pd.DataFrame(
    {'UPC code': [UPC_Code],
     'Book title': [Book_Title],
     'Price excluding tax': [Price_Excluding_Tax],
     'Price including tax': [Price_Including_Tax],
     'Quantity available': [Quantity_Available],
     'Product description': [Product_Description],
     'Category': [Category],
     'Review rating': [Review_Rating],
     'Image URL': [Image_URL],
    }
)

ScottPilgrim.to_csv('ScottPilgrim.csv')

