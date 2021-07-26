import pandas as pd
from pandas.core.frame import DataFrame
import requests 
from bs4 import BeautifulSoup as bs
import numpy as np
import math


class Webscraping:

    def __init__(self, num_items:int, category:str) -> None:
        self.num_items = num_items
        self.category = category

    def extract(self) -> DataFrame:
        """
         A basic web-scraper on scraping Ebay data based on specific category ie dress, bicycle

         Parameters:
        num_items (int): The number of samples (observations) of data to be scraped.
        The minimum samples for scraping is 58, as that is minimum per page

        category(str): The name of the category of which the data is to be scraped.
        Currently only accepts single word as keyword.

        Returns:
        pd.DataFrame: A DataFrame object that has category, author name, title of the category entered,
        price of the category,item URL and image URL for the category item
        """

        titles = []
        prices =[]
        item_urls = []
        image_urls = []


        num_pages = math.ceil(self.num_items/50)
        pages = np.arange(1, num_pages + 1, 1)
        for page in pages:
            url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.category}&_sacat=0&_pgn=" +str(page)
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
            
    
        data = pd.DataFrame(
           {
            "title": titles, "price": prices, "item_url": item_urls, "image_url": image_urls,
           }
        )
    #Clean the data
        data['category_id'] = 1
        data['title'] = data['title'].str.strip().replace("\n", "").replace("\"","")
        data['price'] = data['price'].str.strip()
        data['price'] = data['price'].str.replace("\n","")
            
        return data

scrape = Webscraping(100,'bracelet')
Ebay = scrape.extract()
Ebay.to_csv("Ebay_bracele.csv", index=False,header= True)




