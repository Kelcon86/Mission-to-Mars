# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Set up Splinter, initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_dict": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Article scraping example


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # searching for elements with "div" tag and "list_text" attribute
    # wait one second for page to load

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # div is our parent element to be searched

        # Use the parent element to find the first `div` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# Image scraping example


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    # Index specifies that we want to click the second "button"
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Table scraping example


def mars_facts():

    try:
        # Search for tables in the HTML and only return the first, create a DF
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign column names to the df
    df.columns = ['description', 'Mars', 'Earth']
    # Turn the description column into the DF index
    df.set_index('description', inplace=True)

    # Convert DF back to HTML to keep it dynamic, for use on a webpage
    return df.to_html()

# Hemisphere scrape from Deliverable 1


def hemispheres(browser):
    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_urls = []
    hemisphere_image_urls = []

    try:
        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        # Obtain hemisphere page urls and add to list
        hem_htmls = hemisphere_soup.select('div.description>a')

        for hem_html in hem_htmls:
            href = hem_html['href']
            hemisphere_urls.append(url + href)

        # Loop through page urls, obtain image urls & image titles
        for hem_url in hemisphere_urls:
            browser.visit(hem_url)
            image_url = browser.find_by_text('Sample').first['href']
            image_title = browser.find_by_css('h2').text
            dict_entry = {'img_url': image_url, 'title': image_title}
            hemisphere_image_urls.append(dict_entry)
            browser.links.find_by_partial_text('Back').click()

    except AttributeError:
        return None

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
