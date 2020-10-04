#import dependencies
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

mars = {} 

def init_browser():
    executable_path = {'executable_path':'chromedriver'}
    return Browser('chrome', **executable_path, headless = False)

# main scraping function
def scrape():
    browser = init_browser()
    news_title, news_teaser = mars_news()
    mars = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_img_url": featured_img(), 
        "mars_facts": facts(),
        "hemisphere_img_urls": hemi_urls(),     
    }
    browser.quit()

    return mars

#1. NEWS SCRAPE
def mars_news():
    browser = init_browser()
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
    news_teaser_body = soup.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
    
    return news_title, news_teaser_body    

#2. FEATURED IMG SCRAPE
def featured_img():
    browser = init_browser()
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    time.sleep(1)
    browser.find_by_id('full_image').click()
    time.sleep(1)
    browser.find_link_by_partial_text('more info').click()
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_img_url = soup.find('figure', class_='lede').a['href']
    full_image_url = "https://www.jpl.nasa.gov" + featured_img_url
  
    return full_image_url


#3. MARS FACTS SCRAPING INTO HTML TABLE
def facts():
    url ='https://space-facts.com/mars/'
    facts_df = pd.read_html(url)[0]
    facts_df.columns = ['Description','Mars']
    facts_df.set_index('Description', inplace=True)
    facts_table = facts_df.to_html()

    return facts_table

#4. MARS HEMISPHERES
def hemi_urls():
    browser = init_browser()
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    time.sleep(1) 
    hemisphere_img_urls = []
    html = browser.html
    soup = bs(html, 'html.parser')
    links = soup.find('div', class_='collapsible results').find_all('div',class_='item')

    for each_hemisphere in links:
    
        
        hem_title = each_hemisphere.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
        hem_url = 'https://astrogeology.usgs.gov'
        each_hem_image_url = hem_url + each_hemisphere.find('a',class_='itemLink product-item')['href']
        browser.visit(each_hem_image_url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        full_image_url = soup.find('div',class_='downloads').a['href']    
        each_hemisphere_image = {
            "title" : hem_title,
            "image_url" : full_image_url
        }
        hemisphere_img_urls.append(each_hemisphere_image)
        
        browser.back()

    return hemisphere_img_urls

if __name__ == "__main__":
    
    # If run from shell
    print (scrape())  