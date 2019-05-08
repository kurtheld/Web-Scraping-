from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

def scrape():

    # Create library to hold mission to mars data
    mission_to_mars_data = {}

    # URL from site to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=\
    &category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)

    soup = bs(response.text, 'html5lib')

    news_title = soup.find_all('div', class_ = 'content_title')[0].find('a').text.strip()

    news_p = soup.find_all('div', class_ = 'rollover_description_inner')[0].text.strip()

    executable_path = {'executable_path' : 'C:\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response2 = requests.get(url2)
    browser.visit(url2)

    html = browser.html

    # Create a 2nd BS object
    soup2 = bs(html, 'html5lib')

    #  Scrape for for JPL Featured Space Image
    address = soup2.find_all('a', class_ = 'fancybox')[0].get('data-fancybox-href').strip()

    # Complete featured_image_url w/ address variable just created
    featured_image_url = 'https://www.jpl.nasa.gov/' + address
    browser.visit(featured_image_url)

    # Mars Weather

    # ReTell the directory where Chromedriver is
    executable_path = {'executable_path' : 'C:\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Create 3rd URL to be scraped
    url3 = 'https://twitter.com/marswxreport?lang=en'

    # Make sure it works
    browser.visit(url3)

    html = browser.html
    soup3 = bs(html, 'html5lib')

    mars_weather = soup3.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text


    # Mars Facts
    # create URL #4 to be scraped

    url4 = 'https://space-facts.com/mars/'

    # Use Pandas show the url table
    table = pd.read_html(url4)

    html_table = table[0].to_html()



    # Mars Hemispheres

    # ReTell the directory where Chromedriver is

    executable_path = {'executable_path' : 'C:\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url5)

    html = browser.html
    soup5 = bs(html, "html.parser")

    results = soup5.find_all("h3")

    # Creating and populating Titles dictionary

    titles = []

    for result in results:
        result = str(result)
        result = result[4:-14]
        titles.append(result)

    img_url = []

    for title in titles:
        browser.click_link_by_partial_text(title)
    
        #grabbing html and BS from a few cells above
        html = browser.html
        soup5 = bs(html, "html.parser")
    
        img_url.append(soup5.find('div', class_ = 'downloads').find('a')['href'])    

    hemisphere_image_urls = []

    for title, img_url in zip (titles, img_url):
        hemisphere_image_urls.append({'title': title, 'img_url_url': img_url})

    mission_to_mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mission_to_mars_data