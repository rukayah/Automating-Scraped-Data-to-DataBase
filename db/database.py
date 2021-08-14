import psycopg2
import csv
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Database:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        creates a connection to the database
        
        :return: the cursor that would be use to execute sql command
        """
        self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        return self.cursor


    def create_tables(self):
        """
        creates tables that would sit in the postgre database
        
        :return: the created tables
        """
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category(
            id SERIAL PRIMARY KEY,
            category VARCHAR(50) UNIQUE
        );
        ''' )
        

        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Products(
            id SERIAL PRIMARY KEY,
            title VARCHAR,
            price VARCHAR,
            item_url VARCHAR,
            image_url VARCHAR,
            category_id INTEGER REFERENCES category(id)
            
        );
        ''')
        
    def get_records_from_both_tables(self):
        """
        creates a csv file that contains the joined records from
        products and category tables
        
        :return: a newly created csv file containg all products in the postgres database
        """
        self.cursor.execute(""" SELECT Products.id, title, item_url, image_url, price, category 
                                     FROM Products INNER JOIN Category ON Products.category_id = Category.id""")
        data = self.cursor.fetchall()
        with open('product.csv', 'w', encoding="utf-8") as file:
            csv_file = csv.writer(file)
            csv_file.writerow(["id", "title","item_url", "image_url", "price", "category"])
            csv_file.writerows(data)


    

