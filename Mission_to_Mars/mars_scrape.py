#import dependencies
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

#initialize browser path 
# def init_browser():
#     executable_path = {'executable_path': 'chromedriver'}
#     return Browser('chrome', **executable_path, headless=False) 
mars = {}
#scraping function
def scrape():
    browser = Browser('chrome', executable_path = 'chromedriver', headless=False)
   
    #1. SCRAPE THE NASA NEWS SITE FOR THE FIRST ARTICLE TITLE AND TEASER
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup_news = bs(html, 'html.parser')
    news_title = soup_news.find('div', class_='list_text').find('div', class_='content_title').text
    news_teaser = soup_news.find('div', class_='article_teaser_body').text
    #populate the dictionary
    mars["news_title"] = news_title
    mars["teaser"] = news_teaser

    #2. SCRAPE THE FEATURED IMAGE
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id('full_image').click()
    browser.is_element_present_by_text('more info')
    time.sleep(1)
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    soup = bs(html,'html.parser')
    featured_img_url = soup.select_one('figure.lede a img').get("src")
    featured_img_url
    #populate the dictionary
    mars['featured_image'] = featured_img_url

    #3. SCRAPE THE MARS FACTS
    url = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(url)
    facts = facts_df[0]
    facts = facts.transpose()
    facts_table = facts.to_html(buf=None, columns=None, col_space=None, header=False, index=False, \
                    na_rep='NaN', index_names=False, justify='right', bold_rows=True, classes=None, \
                    escape=True, max_rows=None, max_cols=None, show_dimensions=False, \
                    notebook=False, decimal='.', border=1)
    #populate the dictionary
    mars['facts'] = facts_table

    #4. SCRAPE FOR MARS HEMISPHERES
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    links = soup.find('div', class_='item')
    title = []
    img_urls = []

    for i in links:
        url = "https://astrogeology.usgs.gov" + i.find('a', class_='itemLink product-item')['href']
        browser.visit(url)
        html = browser.html
        soup = bs(html,'html.parser')
        results = soup.find('div', class_='container')
        title.append(results.find('h2',class_ = 'title').text)
        img_urls.append("https://astrogeology.usgs.gov" + results.find('img', class_="wide-image")['src'])

        hemisphere_urls = pd.DataFrame({
            "title":title,
            "url":img_urls
        })
    mars['hemispheres'] = hemisphere_urls
    browser.quit()
    return mars