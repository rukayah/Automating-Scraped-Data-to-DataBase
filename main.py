from src.scraper import Webscraping
from db import Database
from src.products import Products
from src.categories import Category


# How the program should be run
db = Database()
db.connect()
db.create_tables()
scraper = Webscraping()
scraper.extract(num_items = 3000, keyword = "bracelet")
scraper.add_category_to_database()
scraper.add_products_to_database()
db.get_records_from_both_tables()
db.connect().close()