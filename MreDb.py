import MySQLdb
import ConnectionInfo

class MreDb:

    def __init__(self):
        self.data = {}

        self.db = MySQLdb.connect(host=connectionInfo.host,
            user=connectionInfo.user,
            passwd=connectionInfo.passwd,
            db=connectionInfo.db)
        self.cursor = self.db.cursor()
        return

    def clearDatabase(self):
        self.cursor.execute("DELETE FROM production_year")
        self.cursor.execute("DELETE FROM menu")
        self.cursor.execute("DELETE FROM menu_to_year")
        self.cursor.execute("DELETE FROM menu_to_items")
        self.cursor.execute("DELETE FROM menu_item")
        return self

    def addProductionYear(self, yearName):
        self.cursor.execute("INSERT INTO production_year (name) VALUES (:yearName)", {'yearName':yearName})
        self.db.commit()
        return self.cursor.lastrowid

    def addMenu(self, name, yearID):
        self.cursor.execute(
            "INSERT INTO menu (name) VALUES (:name)",
            {"name":name})
        menuID = self.cursor.lastrowid
        self.cursor.execute(
            "INSERT INTO menu_to_year (menu_id, year_id) VALUES (:menu_id, :year_id)",
            {"menu_id":menuID, "year_id":yearID})
        self.db.commit()
        return menuID

    def addMenuItem(self, itemName, mainMeal, menuID):
        self.cursor.execute(
            "INSERT INTO menu_item (name, main_meal) VALUES (:name, :mainMeal)",
            {"name":itemName,"mainMeal":mainMeal})

        itemID = self.cursor.lastrowid

        self.cursor.execute(
           "INSERT INTO menu_to_items (menu_id, item_id) VALUES (:menuID, :itemID)",
           {"menuID":menuID,"itemID":itemID})

        self.db.commit()
        return itemID
