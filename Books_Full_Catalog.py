import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from Book_Category_Scrape import scrape_category

#url this whole process will be based around
catalog_url = "https://books.toscrape.com/index.html"
page = requests.get(catalog_url)
page.raise_for_status()
soup = BeautifulSoup(page.content, "html.parser")

#for loop that will run the scrape_category function for each category, pulling all information for all books and saving them to a different CSV file for each category
for link in soup.select("ul.nav.nav-list > li > ul a[href]"):
    #Strips the text from each iteration of "a[href]" that was listed in the for loop. This text will be used to create the name for the CSV file
    category_name = link.get_text(" ", strip=True)
    #strips the url from the [href] section for each iteration of link, which will be used in the Book_Category_Scrape.py script
    category_url = urljoin(page.url, link["href"])
    #creates the CSV file name based on the category name
    csv_filename = f"{category_name}.csv"
    
    #calls upon the scrape_category function from Book_Category_Scrape.py, gives it the category_url and csv_filename, and allows it to scrape all books within that category and save them to the CSV file
    scrape_category(category_url, csv_filename)
    #prints a message telling the user that each category was successfully scraped adn saved to csv files
    print(f"Saved {category_name} books to {csv_filename}")
