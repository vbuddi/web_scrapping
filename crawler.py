import requests
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import Workbook


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
main_url = "https://azuremarketplace.microsoft.com"

try:
    result = requests.get(main_url, headers = headers)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

path = "test.xlsx"

df = pd.DataFrame(columns=['Url','Title', 'Description'])

app_urls = []

soup = BeautifulSoup(result.content, 'html5lib')

#print(soup.prettify())

try:
    table = soup.find('div', attrs = {'class':'slick-list'})
except Exception as ex:
    print(ex)
    raise

#print(table)

try:
    for row in table.find_all('div', attrs = {'class':'spza_tileWrapper'}):
        app_urls.append(row.a['href'])
except Exception as ex:
    print(ex)
    raise

try:
    for item in app_urls:
        app_url = main_url + item
        print(app_url)
        app_webpage = requests.get(app_url, headers = headers)
        app_soup = BeautifulSoup(app_webpage.content, 'html5lib')
        
        #print(app_soup) # comment it out

        page_content1 = app_soup.find('div', {'class': 'deatilPageContent'})
        page_content2 = app_soup.find('div', {'class': 'description'})

        #print(page_content1.h1.text)
        #print(page_content2.text)

        print('----------------------------------------')

        df = df.append({'Url' : app_url, 'Title' : page_content1.h1.text, 'Description' : page_content2.text}, ignore_index = True)

        #print(df)
except IOError as ex:
    print('Couldn''t find the class element' )
except Exception as ex:
    print(ex)
else:
    #print(df)
    df.to_excel('test.xlsx', sheet_name='crawler')

