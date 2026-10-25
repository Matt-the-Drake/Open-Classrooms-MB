import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from Single_Book_Scrape import scrape_book
page = requests.get('https://books.toscrape.com/catalogue/category/books/travel_2/index.html')
page.raise_for_status()
soup = BeautifulSoup(page.content, 'html.parser')

#creates a list to input all information from each book
all_books = []

#for loop calls upon the section of the page with each individual book html address ("h3 a[href]")
for link in soup.select("h3 a[href]"):
    #joins the partial url from the previous pull with the page url, creating a functional url for each book
    book_url = urljoin(page.url, link["href"])
    #scrapes the currently selected book for all information utilizing the "scrape_book" function created in the Single_Book_Scrape python code
    book_data = scrape_book(book_url)
    #appends the list created above this loop, which will be used to make the csv file
    all_books.append(book_data)

#creates and appends the csv file using the list created above, which now contains all information for all found books
pd.DataFrame(all_books).to_csv("all_travel_books.csv", index=False)