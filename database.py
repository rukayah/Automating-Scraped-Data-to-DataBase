import psycopg2
import csv
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
connection = psycopg2.connect(os.getenv("DATABASE_URL"))


cur = connection.cursor()

cur.execute('''ALTER TABLE product_joined DROP COLUMN categoryname;''')
connection.commit()

cur.execute(
'''CREATE TABLE Product_joined AS
SELECT * FROM products JOIN category ON products.category_name = category.categoryname;
''')
connection.commit()

cur.execute("DROP TABLE IF EXISTS category;")
cur.execute('''
CREATE TABLE category(
    category_id SERIAL PRIMARY KEY,
    categoryname VARCHAR(50)
);
''' )
cur.execute('''
INSERT INTO category (categoryname) VALUES('dress');
INSERT INTO category (categoryname) VALUES('bag');
INSERT INTO category (categoryname) VALUES('bracelet');
''')
connection.commit()
cur.execute("DROP TABLE IF EXISTS products;")
cur.execute(''' 
CREATE TABLE products(
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    price VARCHAR,
    item_url VARCHAR,
    image_url VARCHAR,
    category_name VARCHAR
    
);
''')


with open('Ebay_dress.csv','r',encoding="utf8") as f:
    cur.copy_expert('COPY products(title,price,item_url,image_url,category_name) FROM STDIN WITH HEADER CSV',f)
connection.commit()



