import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

import pymongo

#setup mongo db
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
mars_db = db.mars 

def scrape():
    #nasa news scraping_________
    #create browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit the browser
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #html parsing for bs
    html = browser.html
    soup = bs(html, 'html.parser')

    #get all results for each row
    result = soup.find_all('div', class_='row')

    #always search for 0 to grab the first one, could do just .find as well
    title = result[0].find('div', class_='content_title').text
    paragraph = result[0].find('div', class_='article_teaser_body').text

    #image scrape____________
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)

    #parse html
    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.find('a',class_='showimg fancybox-thumbs')
    featured_image_url = img_url + image_url.get('href')

    #mars facts____
    mars_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    table = pd.read_html(mars_url)
    mars_earth_df = table[0]
    mars_earth_df.rename(columns={0:'Description',1:'Mars',2:'Earth'},inplace=True)
    mars_earth_df.set_index('Description',inplace=True)
    mars_df_dict = mars_earth_df.to_dict('records')

    #mars hemispheres
    mars_hem_url = 'https://marshemispheres.com/'
    browser.visit(mars_hem_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div',class_='item')

    hemisphere_image_urls = []

    for result in results:
        result_dict = {}
        title = result.find('h3').text
        href_link = result.find('a')['href']
        img_link = mars_hem_url + href_link

        browser.visit(img_link)

        html = browser.html
        soup = bs(html, 'html.parser')

        download_block = soup.find('div',class_='downloads')
        img_url = mars_hem_url + download_block.find('a')['href']
        #print(img_url)
        #put into dict and then append to list
        result_dict['title'] = title
        result_dict['img_url'] = img_url
        hemisphere_image_urls.append(result_dict)

    browser.quit()


    #import into mongo
    mars_data ={
        'news_title': title,
        'news_p': paragraph,
        'featured_image_url': featured_image_url,
        'mars_fact_table': mars_df_dict,
        'mars_hemispheres': hemisphere_image_urls
    }
    
    # mars_db.insert_many([mars_data])
    return mars_data