from bs4 import BeautifulSoup
from lxml import html
import os
import uuid
import requests
import re

'''
This function pulls the list of MRE production years from mreinfo.com
and then downloads the page for each production year.  It returns an array
containing the html from each MRE production year page.
'''
def crawlYears(self):
    # Initialize the array so it works with append.
    productionYearSoup = []

    # Get the page listing al MRE prduction years.
    html = requests.get('http://www.mreinfo.com/us/mre/mre-menus.html')
    print('Downloaded production year list.')

    # Find all of the links in the table containing the production year list.
    soup = BeautifulSoup(html.text, 'lxml')
    urls = soup.find('table', 
            attrs={'border':'1','width':'100%'}).find_all('a')

    # Iterate over the urls and download the page for each production year.
    for url in urls:
        html = requests.get(url['href']).text
        soup = BeautifulSoup(html, 'lxml')
        productionYearSoup.append(soup)
        print('Downloaded html for a production year.')

    return productionYearSoup

'''
This function writes the iterable soupList to a file with a random name in
path.  This is used to store the data pulled from mreinfo.com to prevent
downloading the same pages over and over.
'''
def write( path, soupList):

    # Create the directory if it doesn't exist.
    # Note that this will crash if the permissions are bad or if there is a 
    # regular file with the same name as the specified directory.
    if not os.path.exists(path):
        os.makedirs(path)

    # Iterate over soupList
    for item in soupList:
        # Create a random filename with html extension
        filename = path + uuid4() + '.html'
        f = open(filename, 'w')
        f.write(item.prettify().encode('utf-8'))
        f.close()

'''
Get the title from the page for an MRE production year.
'''
def getYearTitle(yearPage):
    return yearPage.find_all("h1")[0].text

'''
Get the menu title.
TODO: This returns a random menu item.
'''
def getMenuTitle(menu):
    return getMenuItems(menu)[0]

'''
This function loads html files from the specified path and returns an array.
The array conntains a beautiful soup object, not html text.
'''
def load( path):
    # Initialize the array so it's ready for append()
    soupList = []

    # This will crash if path does not exist or user does not have permissions.
    fileList = os.listdir(path)

    for filename in fileList:

        # Ignore the file if it is a directory.
        if not os.path.isdir(os.path.join(path,filename)):
            # Open and read the file..
            f = open(path+filename, 'r')
            html = f.read()
            f.close()
            print('Read '+filename)

            # Convert it to soup
            soup = BeautifulSoup(html, 'lxml')
            soupList.append(soup)

    return soupList

'''
Get all of the menus from a production year page.  The argument is a soup
object.  This returns the html text (not soup) from the menu <td>.
'''
def getMenus( productionYear):
    # Create the array so it's ready for append.
    menus = []
    yearTitle = getYearTitle(productionYear)

    # Find all the menus
    menuFilter = getMenuFilter(yearTitle)
    menuSoup = menuFilter(productionYear)
    for menu in menuSoup:
        menus.append(menu.text)

    return menus

'''
Get a function that returns the beautiful soup selector to get the menu for
the specified year.
'''
def getMenuFilter(yearTitle):
    # Use a dict to map yearTitles to filter functions
    menuFilter = {
        u'MRE Menus I (1981) - MRE V (1985)': '',
        u'MRE Menus XIX (1999)': '',
        u'MRE Menus VI (1986)': '',
        u'MRE Menus VII (1987)': '',
        u'MRE Menus VIII (1988) - MRE IX (1989)': '',
        u'MRE Menus X (1990) - MRE XI (1991)': '',
        u'MRE Menus XII (1992)': '',
        u'MRE Menus XIII (1993) - XIV (1994)': '',
        u'MRE Menus XV (1995)': '',
        u'MRE Menus XVI (1996)': '',
        u'MRE Menus XVII (1997)': '',
        u'MRE Menus XVIII (1998)': '',
        u'MRE Menus XX (2000)': '',
        u'MRE Menus XXI (2001)': '',
        u'MRE Menus XXII (2002)': '',
        u'MRE Menus XXIII (2003)': '',
        u'MRE Menus XXIV (2004)': '',
        u'MRE Menus XXV (2005)': '',
        u'MRE Menus XXVI (2006)': '',
        u'MRE Menus XXVII (2007)': '',
        u'MRE Menus XXVIII (2008)': '',
        u'MRE Menus XXIX (2009)': menus2009to2014,
        u'MRE Menus XXX (2010)': menus2009to2014,
        u'MRE Menus XXXI (2011)': menus2009to2014,
        u'MRE Menus XXXII (2012)': menus2009to2014,
        u'MRE Menus XXXIII (2013)': menus2009to2014,
        u'MRE Menus XXXIV (2014)': menus2009to2014,
    }.get(yearTitle) # Get the dict entry for the specified year
    return menuFilter

'''
Get the menu entry for 2009-2014.
'''
def menus2009to2014(year):
    soup = year.find_all('td', attrs={'valign':'top','width':'25%'})
    return soup

'''
Pull the menu items out of the html from a menu.  This works on html text,
not soup.  The return value is an array of strings.
'''
def getMenuItems(menu):

    # Remove the tabs and rejoin the menu items.
    notabs = ''.join(menu.split('\t'))

    # Split into an array on the newlines.
    menuItems = notabs.split('\n')

    # The first record is empty from the string operations.
    #del menuItems[0]

    return menuItems

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

