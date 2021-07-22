import pandas as pd
from pandas.core.accessor import PandasDelegate
from pandas.core.frame import DataFrame
import requests # this is used to get the data from the website
from bs4 import BeautifulSoup as bs
import numpy as np
import time
import math



def extract(num_items:int, category:str)-> DataFrame:

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


    num_pages = math.ceil(num_items/50)
    pages = np.arange(1, num_pages + 1, 1)
    for page in pages:
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={category}&_sacat=0&_pgn=" +str(page)
        source = requests.get(url).text
        soup = bs(source, "lxml")
        print(page)

        for dress in soup.find_all('li',class_='s-item--watch-at-corner'):
            title = dress.h3.text
            titles.append(title)
            price = dress.find('span',class_='s-item__price').text
            prices.append(price)
            item_url = dress.find('a', class_='s-item__link')['href']
            item_urls.append(item_url)
            image_url = dress.find('img', class_='s-item__image-img')['src']
            image_urls.append(image_url)
            time.sleep(2) 
    
    data = pd.DataFrame(
        {
            "Title": titles, "Prices": prices, "Item_url": item_urls, "Image_url": image_urls,
        }
    )
    #Clean the data
    data['Category'] = category
    data['Category'] = data['Category'].str.capitalize()
    data['Title'] = data['Title'].str.strip().replace("\n", "").replace("\"", "")
    data['Prices'] = data['Prices'].str.strip()
    data['Prices'] = data['Prices'].str.replace("\n", "")
            
    return data

Ebay = extract(3000,'bracelet')
Ebay.to_csv("Ebay_bracelet.csv", index=False,header= True)



