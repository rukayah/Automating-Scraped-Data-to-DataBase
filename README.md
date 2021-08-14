# Web-Scraper

A basic web-scraper on scraping Ebay data based on specific category ie dress, bicycle

        Parameters:
        num_items (int): The number of samples (observations) of data to be scraped.
        The minimum samples for scraping is 58, as that is minimum per page

        keyword (str): The name of the category of which the data is to be scraped.
        Currently only accepts single word as keyword.

        Returns:
        pd.DataFrame: A DataFrame object that has category, author name, title of the category entered,
        price of the category,item URL and image URL for the category item

