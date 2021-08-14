from src.products import Products
from src.categories import Category
import pandas as pd
from pandas.core.frame import DataFrame
import requests 
from bs4 import BeautifulSoup as bs
import numpy as np
import math


class ScraperError(Exception):
    "Error handling class for all thing related to webscraping"
    pass

class Webscraping:

    def __init__(self) -> None:
        self.dataframe = None
        self.keyword = None

    def extract(self,num_items:int, keyword:str) -> DataFrame:
        """
         A basic web-scraper on scraping Ebay data based on specific category ie dress, bicycle

        Parameters:
        num_items (int): The number of samples (observations) of data to be scraped.
        The minimum samples for scraping is 58, as that is minimum per page

        keyword (str): The name of the category of which the data is to be scraped.
        Currently only accepts single word as keyword.

        Returns:
        pd.DataFrame: A DataFrame object that has category, author name, title of the category entered,
        price of the category,item URL and image URL for the category item
        """
        self.keyword = keyword

        titles = []
        prices =[]
        item_urls = []
        image_urls = []


        num_pages = math.ceil(num_items/50)
        pages = np.arange(1, num_pages + 1, 1)
        for page in pages:
            url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.keyword}&_sacat=0&_pgn=" +str(page)
            source = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"}).text
            soup = bs(source, "lxml")
        #print(page)

            for dress in soup.find_all('li',class_='s-item--watch-at-corner'):
                title = dress.h3.text
                titles.append(title)
                price = dress.find('span',class_='s-item__price').text
                prices.append(price)
                item_url = dress.find('a', class_='s-item__link')['href']
                item_urls.append(item_url)
                image_url = dress.find('img', class_='s-item__image-img')['src']
                image_urls.append(image_url)
            
        
        self.dataframe = pd.DataFrame(
           {
            "title": titles, "price": prices, "item_url": item_urls, "image_url": image_urls,
           }
        )
        self.dataframe['title'] = self.dataframe['title'].str.strip().replace("\n", "").replace("\"","")
        self.dataframe['price'] = self.dataframe['price'].str.strip()
        self.dataframe['price'] = self.dataframe['price'].str.replace("\n","")
            
        return self.dataframe


  
    def add_category_to_database(self):
        """
        adds the scraped category to the Category Database
        """
        try:
            category_database = Category()
            category_database.add(self.keyword)
            print(f".......{self.keyword} category successfully added to Database.......")
            self.category_id = category_database.get_by_name(self.keyword)[0]
        except ScraperError:
            raise ScraperError(f"Category {self.keyword} is already in the database")

    def add_products_to_database(self):
        """
        adds scraped products of keyword to products database
        :return: products successfully added message.
        """
        try:
            self.dataframe['category_id'] = [self.category_id for each_element in range(len(self.dataframe))]
            product_database = Products()
            product_database.add(self.dataframe)
            print(f"........{self.keyword} products successfully added to Database.......")
        except ScraperError:
            raise ScraperError("This product is already in the database")




