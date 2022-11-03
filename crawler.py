import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
main_url = "https://azuremarketplace.microsoft.com/marketplace/apps"
base_url="https://azuremarketplace.microsoft.com"

result = requests.get(main_url, headers = headers)

path = "scrap_data.xlsx"

df = pd.DataFrame(columns=['Url','Title', 'ShortDescription'])

app_urls = []
categories_url_list = []
sub_category_url_list = []

# Crawl the main URL
soup = BeautifulSoup(result.content, 'html5lib')

#print(soup.prettify())

# get all the categories
categories = soup.find('div', attrs = {'class':'spza_filterContainer'})

#print(categories)

# Create a list with all the category URLs
for row in categories.find_all('a', {"href" : re.compile('/marketplace/apps/category.*')}):
    #print(row['href'])
    categories_url_list.append(base_url + row['href'])

#print(categories_url_list)

# scrape through each category and find the subcategories
# store all the sub categories URLs in a list
try:
    for category_url in categories_url_list:
        sub_category_result = requests.get(category_url, headers = headers)
        category_soup = BeautifulSoup(sub_category_result.content, 'html5lib')
        for sub_category in category_soup.find_all('a', {'href' : re.compile('subcategories=.*')}):
            sub_category_url_list.append(base_url + sub_category['href'])
except IOError as ex:
    print('Couldn''t find the sub category class')
except Exception as ex:
    print(ex)

print(len(sub_category_url_list))
count = 1
try:
    tmp = []
    # for each sub category scrapthe deatils like URL, Title, short description
    # store the details in a data frame to write to excel
    for sub_cat in sub_category_url_list:
        # if sub_cat.find('web-apps') > 0:
        #     continue
        sub_category_result = requests.get(sub_cat, headers = headers)
        sub_category_soup = BeautifulSoup(sub_category_result.content, 'html5lib')
        #for item in sub_category_soup.find_all('a', { 'href' : re.compile(''))
        #print(sub_category_soup)
        page_content1 = sub_category_soup.find('div', {'class': 'tileContent'})
        page_content2 = sub_category_soup.find('div', {'class': 'c-paragraph-4 description'})
        
        # tmp.append({'Url' : sub_cat, 'Title' : page_content1.h3.text, 'ShortDescription' : page_content2.text})
        df = df.append({'Url' : sub_cat, 'Title' : page_content1.h3.text, 'ShortDescription' : page_content2.text}, ignore_index = True)
        #handoffURL = sub_category_soup.find('div', {'handofURL': ''})
        app_data = sub_category_soup.find('div', attrs = {'class':'spza_tileWrapper'})
        app_url = app_data.find('a', href=True)

        #data-bi-name
        # print('---------------------------------------------------------')
        # print(sub_cat)
        # print(page_content1.h3.text)
        # print(page_content2.text)
        # just take only one app URL in a subcategory to scrape the data. This is only for testing
        if count == 1:
        # print(base_url + app_url['href'])
            app_urls.append(base_url + app_url['href'])
            count = count + 1

    print(df)
    df.to_excel('scraper_data.xlsx', sheet_name='crawler')

    # crawl for each app and scrape the deatils
    for url in app_urls:
        app_data = requests.get(url, headers = headers)
        app_data_soup = BeautifulSoup(app_data.content, 'html5lib')
        #print(app_data_soup)
       # page_content = app_data_soup.find('div', {'class': 'deatilPageContent'})
        page_content = app_data_soup.find('div', {'class': 'description'})
        print(page_content.text)

except IOError as ex:
    print('Couldn''t find the class element' )
except Exception as ex:
    print(ex)
else:
    print('Data collection succeeded')
