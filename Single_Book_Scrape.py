import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlsplit


IMAGE_DIR = Path(__file__).resolve().parent / "book_images"

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
    upc_code = table.find("th", string="UPC").find_next("td").get_text(strip=True)
    #finds areticle under "class_="product_page"" which will then be used to get the description and image source (src)
    article = soup.find("article", class_="product_page")
    #finds the section that contains the description of the book
    description = article.find_all('p')[3]
    #finds the image source within the file, which falls under the sixth div element of the article under the class "product_page"
    image_src = article.find_all("div")[5].find("img")["src"]
    #finds the URL for the image by joining the base url of the page with the image source
    image_url = urljoin(page.url, image_src)

    IMAGE_DIR.mkdir(exist_ok=True)
    image_extension = Path(urlsplit(image_url).path).suffix
    image_path = IMAGE_DIR / f"{upc_code}{image_extension}"
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image_path.write_bytes(image_response.content)

    #returns all information gathered, which allows it to be all sorted into a csv file by a different code
    return{
        "Page URL": page.url,
        "UPC code": upc_code,
        "Book title": soup.find(class_="col-sm-6 product_main").find("h1").get_text(strip=True),
        "Price excluding tax": table.find("th", string="Price (excl. tax)").find_next("td").get_text(strip=True),
        "Price including tax": table.find("th", string="Price (incl. tax)").find_next("td").get_text(strip=True),
        "Quantity available": soup.find("p", class_="instock availability").get_text(strip=True),
        "Product description": description.get_text(strip=True),
        "Category": soup.find("ul", class_="breadcrumb").find_all("li")[3].get_text(strip=True),
        "Review rating": soup.find("p", class_="star-rating").get("class")[1],
        "Image URL": image_url,
        "Image file": str(image_path),
    }
