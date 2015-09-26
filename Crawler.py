from bs4 import BeautifulSoup
from lxml import html
import uuid
import requests
import re

class Crawler:

    def __init__(self):
        self.data = {}
        return

    def crawl(self):
        yearRE = re.compile('(\d{4})')
        for year in self.getProductionYears():
            match = yearRE.search(year['title'])
            if match and int(match.group()) >= 2009:
                self.data[year['title']] = {}
                menus = self.getMenus(year['soup'])
                for menu in menus:
                    items = self.getMenuItems(menu['soup'])
                    self.data[year['title']][menu['title']] = items
        return self.data

    '''
    This function pulls the list of MRE production years from mreinfo.com
    and then downloads the page for each production year.  It returns an array
    containing the html from each MRE production year page.
    '''
    def crawlYears(self):
        # Initialize the array so it works with append.
        productionYears = []

        # Get the page listing al MRE prduction years.
        html = requests.get('http://www.mreinfo.com/us/mre/mre-menus.html')
        print('Downloaded production year list.')

        # Find all of the links in the table containing the production year list.
        soup = BeautifulSoup(html.text, 'lxml')
        urls = soup.find('table', 
                attrs={'border':'1','width':'100%'}).find_all('a')

        # Iterate over the urls and download the page for each production year.
        for url in urls:
            ProductionYears.append(requests.get(url['href']).text)
            print('Downloaded html for a production year.')

        return ProductionYears

    '''
    This function writes the iterable itemList to a file with a random name in
    path.  This is used to store the data pulled from mreinfo.com to prevent
    downloading the same pages over and over.
    '''
    def write(self, path, itemList):

        # Create the directory if it doesn't exist.
        # Note that this will crash if the permissions are bad or if there is a 
        # regular file with the same name as the specified directory.
        if not os.path.exists(path):
            os.makedirs(path)

        # Iterate over itemList
        for item in itemList:
            # Create a random filename with html extension
            filename = path + uuid4() + '.html'
            f = open(filename, 'w')
            f.write(item.encode('utf-8'))
            f.close()
