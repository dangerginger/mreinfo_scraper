from bs4 import BeautifulSoup
from lxml import html
import re

class Parser:

    def __init__(self):
        self.data = {}
        return

    def parseMres(self):
        for year in self.loadProductionYears():
            self.data[year['title']] = {}
            menus = self.getMenus(year['soup'])
            for menu in menus:
                items = self.getMenuItems(menu['soup'])
                self.data[year['title']][menu['title']] = items
        return self

    def writeDataToDB(self):

        for year in self.data.keys():
            yearID = self.addProductionYear(year)
            for menu in self.data[year].keys():
                menuID = self.addMenu(menu,yearID)
                for item in self.data[year][menu]:
                    self.addMenuItem(item,False,menuID)
        return self

