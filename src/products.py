from db import Database
import pandas as pd
import psycopg2.extras as extras

class ProductError(Exception):
    """
    Error handling class for all thing related to Product
    """
    pass
class Products:

    def __init__(self, cursor=Database().connect()):
        self.cursor = cursor

    def all(self):
        """
            Gets all rows in the Product Table from the database.
            :return: list containing all records of Products.
        """
        self.cursor.execute("SELECT * FROM Products")
        return self.cursor.fetchall()

    def add(self, df: pd.DataFrame):
        """
            Adds new record to the Products Database records.
            :param details:a dictionary that contains the title,
            category, image url, item url, price of a Product.
            :return: Record successfully added to Database message.
        """
        try:
            
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s)" % ('Products', cols)
            extras.execute_batch(self.cursor, query, tuples, len(df))
            print("Record successfully added to Products")
        except ProductError:
            raise ProductError("Something went wrong when trying to add record(s)")
        
    