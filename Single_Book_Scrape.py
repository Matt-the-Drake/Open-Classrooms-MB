import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#Creates a function to be called upon inside other codes
def scrape_book(book_url):
    #Gets the book url from codes this is used in
    page = requests.get(book_url)
    #checks whether the HTML page is loaded correctly and returns an error if so; if the page loads correctly then this does nothing
    page.raise_for_status()
    #allows for the content of the web page to be scraped from; also this part can be used to find book title, quantity available, category, and review
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #finds the table that has information, specifically the UPC code and prices
    table = soup.find('table', class_="table table-striped")
    #finds the section that contains the description of the book
    description = soup.find("article", class_="product_page").find_all('p')[3]
    #finds the link to the image, which is incomplete but will be used later to join the url with the page url to create the full link for the image
    image_src = soup.find('div', class_="item active").find("img").get("src")


    #returns all information gathered, which allows it to be all sorted into a csv file by a different code
    return{
        "Page URL": page.url,
        "UPC code": table.find("th", string="UPC").find_next("td").get_text(strip=True),
        "Book title": soup.find(class_="col-sm-6 product_main").find("h1").get_text(strip=True),
        "Price excluding tax": table.find("th", string="Price (excl. tax)").find_next("td").get_text(strip=True),
        "Price including tax": table.find("th", string="Price (incl. tax)").find_next("td").get_text(strip=True),
        "Quantity available": soup.find("p", class_="instock availability").get_text(strip=True),
        "Product description": description.get_text(strip=True),
        "Category": soup.find("ul", class_="breadcrumb").find_all("li")[3].get_text(strip=True),
        "Review rating": soup.find("p", class_="star-rating").get("class")[1],
        "Image URL": urljoin(page.url, image_src),
    }
