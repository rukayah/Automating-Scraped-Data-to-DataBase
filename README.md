# Automating-Scraped-Data-to-DataBase

A basic web-scraper on scraping eBay data based on specific keyword ie dress, bicycle.The web scraper can be found in src/scraper and it contains 3 methods which are extract(), add_category_to_database() and add_product_to_database()

        Parameters:
        num_items (int): The number of samples (observations) of data to be scraped.
        The minimum samples for scraping is 50, as that is minimum per page.

        keyword (str): The name of the category of which the data is to be scraped.
        Currently only accepts single word as keyword.

        Returns:
        pd.DataFrame: A DataFrame object that has title,price of the category,
        item URL,image URL and category for the keyword entered.
        """
        add_category_to_database() and add_product_to_database() adds categories and products to their respective databases.

The scrape data is added to the postgre  database using the db/database file where connection is made, tables for saving the scraped data are created. The Database URL is stored in .env file for protection and the URL is found on postgre heroku.

## Usage
You can run the scraper and add it to the postgre database using the main.py file as shown below

        from src.scraper import Webscraping
        from db import Database
        from src.products import Products
        from src.categories import Category


        # Example of how the program should be run
        db = Database()
        db.connect()
        db.create_tables()
        scraper = Webscraping()
        scraper.extract(num_items = 3000, keyword = "bracelet")
        scraper.add_category_to_database()
        scraper.add_products_to_database()
        db.get_records_from_both_tables()
        db.connect().close()
