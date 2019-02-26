from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "C:\\Users\\Alyza\\GWARL201811DATA3\\02-Homework\\12-Web-Scraping-and-Document-Databases\\Instructions\\Images\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Scrape Mars news
    # Scrape Mars news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

        #Get latest Mars article
    news_title = soup.find('div', class_='content_title').text
    news_body = soup.find('div', class_='article_teaser_body').text

    #Scrape Mars images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get featured image
    feature = soup.find('div', class_='img')
    feature_img = feature.img['src']
    feature_img_url = f'https://www.jpl.nasa.gov{feature_img}'      

    # Scrape Twitter for Mars weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #Get last weather tweet
    mars_weather = soup.find('div', class_='js-tweet-text-container').find('p').text

    # Scrape Mars facts with Pandas
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table.columns = ['Description', 'Value']

    html_table = mars_table.to_html()

    html_table.replace('\n', '')

    #Scrape Mars hemisphere images
    hem_urls =[]

    for x in range(4):
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        click_here= browser.find_by_tag('h3')[x].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hem = soup.find('img', class_='wide-image')['src']
        hem_url = f'https://astrogeology.usgs.gov{hem}'
        hem_title = soup.find('h2', class_='title').text
        hem_title = hem_title.replace(' Enhanced','')
        
        hem_urls.append({"title": hem_title, "img_url": hem_url})
        x+=1

    # Store data in a dictionary
    mars_data = {
        "Latest_Headline": news_title,
        "Latest_Text": news_body,
        "Featured_Image": feature_img_url,
        "Current_Weather": mars_weather,
        "Facts_Table": html_table,
        "Hemisphere_Images": hem_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data








