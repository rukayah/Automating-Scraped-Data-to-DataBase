from db import Database

class Category:
    """
    Handles all database communication to the Category table.
    :param cursor: the connection cursor of the relevant database.
    Contains functions add(), all(), get_by_name()
    """
    def __init__(self, cursor=Database().connect()):
        self.cursor = cursor

    def all(self):
        """
        Gets all rows in the Category Table from the database.
        :return: list containing all records of Category.
        """
        self.cursor.execute("SELECT * FROM Category")
        return self.cursor.fetchall()

    def add(self, category:str):
        """
        Adds new category to the category database.
        :param category: the new category to be added to the database
        :return: Category successfully added message.
        """
        self.cursor.execute(f"INSERT INTO Category (category) VALUES ('{category}') ON CONFLICT DO NOTHING")

    def get_by_name(self, name: str):
        """
        gets a particular category from the database by its name
        :param name: name of category to be extracted
        :return: tuple containing category's info
        """
        self.cursor.execute(f"SELECT * from Category WHERE category = '{name}'")
        return self.cursor.fetchone()