import psycopg2
import csv


connection = psycopg2.connect(
    database="d5h8ma03kkd458",
    user="ghalrqkugwlekk",
    password="4ab70c85f384769258ac6a6414a98e8a293ad80a084fff18d644ae33ef3a8e15",
    host="ec2-54-74-77-126.eu-west-1.compute.amazonaws.com",
    port="5432"
)

cur = connection.cursor()

cur.execute('''
CREATE TABLE bracedata(
    title varchar(255),
    price varchar(255),
    item_url varchar(500),
    image_url varchar(225),
    category varchar(255)
);
''')
connection.commit()

cur = connection.cursor()

with open('Ebay_bracelet.csv','r',encoding="utf8") as f:

  next(f)
  cur.copy_from(f, 'bracedata', sep =",")
connection.commit()

cur.execute("SELECT * FROM bracedata")
rows = cur.fetchall()
#rows = cur.fetchone()
for row in rows:
    print(f"title: {row[0]}, price: {row[1]},item_url: {row[2]},image_url: {row[3]},category: {row[4]},")
    