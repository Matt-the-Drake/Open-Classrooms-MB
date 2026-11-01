import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from Single_Book_Scrape import scrape_book

#Creates a function to be utilezed later to scrape all categories from teh webpage, utilizing category_url and csv_filename from the next fucntion call, which will then be used to scrape all the books individually for data 
def scrape_category(category_url, csv_filename):
    #creates a list to input all information from each book
    all_books = []
    current_url = category_url

    #while loop that dictates which single book in the category will be scraped currently, while there is content assigned to "curent_url" the while loop will continue
    while current_url:
        #Calls upon the category url pulled from the Books_Full_Catalog.py script
        page = requests.get(current_url)
        #Checks to see if "page" was successful in getting a proper HTTP address, if not it gives an error
        page.raise_for_status()
        #Makes it so that each "current_url" can be parsed and tehrefore can be scraped from
        soup = BeautifulSoup(page.content, "html.parser")

        #for loop calls upon the section of the page with each individual book html address ("h3 a[href]")
        for link in soup.select("h3 a[href]"):
            #joins the partial url from the previous pull with the page url, creating a functional url for each book, and assigns it to book_url to be used by Single_Book_Scrape.py script
            book_url = urljoin(page.url, link["href"])
            #appends the list created above this loop, which will be used to make the csv file
            all_books.append(scrape_book(book_url))

        #Looks inside the "li" part of the HTML code, selecting the next a[href] in order
        next_page = soup.select_one("li.next a[href]")
        #moves through the "current_content" one at a time, eventually setting "curretn_url" to "None" when there are no more pages to list
        current_url = urljoin(page.url, next_page["href"]) if next_page else None

    pd.DataFrame(all_books).to_csv(csv_filename, index=False)
    return all_books
