import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import warnings
from random import randint
from time import sleep
warnings.simplefilter(action='ignore', category=FutureWarning)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
main_url = "https://azuremarketplace.microsoft.com/marketplace/apps"
base_url="https://azuremarketplace.microsoft.com"

result = requests.get(main_url, headers = headers)

path = "scrap_data.xlsx"

df = pd.DataFrame(columns=['Category', 'Sub_Category', 'App_Title', 'App_Url', 'ShortDescription', 'Desription', 'Pricing', 'Reviews'])

app_urls = []
categories_url_list = []
all_sub_category_url_list = []
category_subcat_url_dict = {}
category_subcat_dict = {}
all_sub_cat_page_url_list_new = []
all_app_url_list = []

# Crawl the main URL
soup = BeautifulSoup(result.content, 'html.parser')

# print(soup.prettify())

# get all the categories
categories = soup.find('div', attrs = {'class':'spza_filterContainer'})

# print(categories)

# Create a list with all the category URLs
for row in categories.find_all('a', {"href" : re.compile('/marketplace/apps/category.*')}):
    #print(row['href'])
    categories_url_list.append(base_url + row['href'])

# print((categories_url_list)) 
# Total 21 Categories 
# ex: 'https://azuremarketplace.microsoft.com/en-us/marketplace/apps/category/analytics?page=1, https://azuremarketplace.microsoft.com/en-us/marketplace/apps/category/ai-plus-machine-learning?page=1

# scrape through each category and find the subcategories
# store all the sub categories URLs in a list
try:
    for category_url in categories_url_list:
        idx1 = category_url.index('category/')
        idx2 = category_url.index('?')
        category_name = category_url[idx1 + len('category/') : idx2]
        # print('\n\n')
        # print(category_name)
        # print(category_url)
        sub_category_result = requests.get(category_url, headers = headers)
        category_soup = BeautifulSoup(sub_category_result.content, 'html.parser')
        sub_category_name = ''
        sub_category_url_list = []
        category_subcat_url_dict[category_name] = []
        category_subcat_dict[category_name] = []
        #print(category_soup.find_all('a', {'href' : re.compile('subcategories=.*')}))
        # # # subcategories_data = category_soup.find_all('a', {'href' : re.compile('subcategories=.*')})
        # # # subcategory_list = subcategories_data.findall('a', {'aria-label' : re.compile('see all for*')})
        # print('----------------------------------')
        for sub_category in category_soup.find_all('a', {'href' : re.compile('subcategories=.*')}):
            sub_category_url = sub_category['href']
            # if href contains '=all', skip it as we are collecting all subcategories data
            if '=all' in sub_category_url:
                continue
            sub_category_url_list.append(base_url + sub_category_url)
            all_sub_category_url_list.append(base_url + sub_category_url)
            idx3 = sub_category_url.index('subcategories=')
            sub_category_name = sub_category_url[idx3 + len('subcategories=') : len(sub_category_url)]
            category_subcat_dict[category_name].append(sub_category_name)
        x = randint(1,3)
        sleep(x)
        sub_category_url_list = list(dict.fromkeys(sub_category_url_list))
        # print(sub_category_url_list)
        category_subcat_url_dict[category_name].append(sub_category_url_list)
        all_sub_category_url_list = list(dict.fromkeys(all_sub_category_url_list))
except IOError as ex:
    print(ex)
# except Exception as ex:
#     print(ex)
print((all_sub_category_url_list))
#print(category_subcat_url_dict)
#print(category_subcat_dict)

subcat_app_url_dict = {}
sub_cat_page_urls_list = []

# Find all the pages for each sub category
try:
    for sub_cat_url in all_sub_category_url_list:
        idx1 = sub_cat_url.index('category/')
        idx2 = sub_cat_url.index('?')
        category_name = sub_cat_url[idx1 + len('category/') : idx2]

        idx3 = sub_cat_url.index('subcategories=')
        sub_category_name = sub_cat_url[idx3 + len('subcategories=') : len(sub_cat_url)]
        subcat_app_url_dict[category_name+'|'+sub_category_name] = []
        sub_cat_page_urls_list = []
        for i in range(1,50):
            new_sub_cat_url = re.sub('page=?(.*?)&', 'page='+str(i)+'&', sub_cat_url)

            app_price_data = requests.get(new_sub_cat_url, headers = headers)
            app_price_data_soup = BeautifulSoup(app_price_data.content, 'html.parser')

            data = app_price_data_soup.find('div', {'class': 'filteredGalleryContainer'})

            if data == None:
                #print('Tag filteredGalleryContainer not found, this is not valid page')
                break
            else:
                sub_cat_page_urls_list.append(new_sub_cat_url)
                all_sub_cat_page_url_list_new.append(new_sub_cat_url)
        x = randint(1,5)
        sleep(x)
        sub_cat_page_urls_list = list(dict.fromkeys(sub_cat_page_urls_list))
        subcat_app_url_dict[category_name+'|'+sub_category_name] = sub_cat_page_urls_list
        #print(sub_cat_page_urls_list)
    print(subcat_app_url_dict)
except Exception as ex:
    print(ex)

i = 0
for idx, (key, page_urls) in enumerate(subcat_app_url_dict.items()):

    if (idx  >= 0 and idx <= 10):
        temp = key.split('|')
        category = temp[0]
        sub_cat = temp[1]
        #print(cat + '---' + sub_cat)
        count = 0
        for page_item in page_urls:
            print(page_item)
            x = randint(1,10)
            sleep(x)
            if count == 50:
                sleep(x)
                count = 0
            page_data = requests.get(page_item, headers = headers)
            #print(page_data.status_code)
            page_data_soup = BeautifulSoup(page_data.content, 'html.parser')

            for tile in page_data_soup.find_all('a', attrs={'class': 'tileLink'}):
                all_app_url_list.append(base_url + tile['href'])
                title = tile.find('div', {'class': 'tileContent'})
                short_description = tile.find('div', {'class': 'description'})
                df = df.append({'Category' : category, 'Sub_Category': sub_cat, 'App_Url' : base_url + tile['href'], 'App_Title' : title.h3.text, 'ShortDescription' : short_description.text}, ignore_index = True)
                

all_app_url_list = list(dict.fromkeys(all_app_url_list))
print(all_app_url_list)
print(len(all_app_url_list))

count = 0
for url in all_app_url_list:
    x = randint(1,10)
    sleep(x)
    if count == 50:
        sleep(x)
        count = 0
    count += 1
    app_data = requests.get(url, headers = headers)
    app_data_soup = BeautifulSoup(app_data.content, 'html.parser')
    #print(url)
    page_content = app_data_soup.find('div', {'class': 'deatilPageContent'})
    #page_content = app_data_soup.find('div', {'class': 'description'})
    app_id = re.search('apps/(.*)\?', url).group(1)
    prices_url = 'https://azuremarketplace.microsoft.com/view/appPricing/{}/us?ReviewsMyCommentsFilter=true'.format(app_id)
    reviews_url = 'https://azuremarketplace.microsoft.com/view/app/{}/reviews'.format(app_id)

    pricing_data = requests.get(prices_url, headers = headers).json()["skus"]

    review_response = requests.get(reviews_url, headers = headers)

    review_response_soup = BeautifulSoup(review_response.content, 'html.parser')
    #print(type(page_content.text))
    df_row = df['App_Url'] == url
    #print(df_row)
    df.loc[df_row, 'Pricing'] = json.dumps(pricing_data)
    df.loc[df_row, 'Reviews'] = str(review_response_soup)
    df.loc[df_row, 'Desription'] = page_content.text

print(df)
df.to_excel('analytics_data-insights.xlsx', sheet_name='crawler')

