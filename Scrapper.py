from bs4 import BeautifulSoup
from selenium import webdriver
from mongo import Mongo
import logging as log
from dotenv import load_dotenv
load_dotenv()
import os

log.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class Scrapper():
    def __init__(self, start_page = 1, start_index = 0) -> None:
        self.start_page = start_page
        self.start_index = start_index
    
    BASE_URL = "https://www.ultimate-guitar.com/explore?type[]=Chords&page={}"
    db = Mongo()
    
    def scrape (self):
        for page in range(13, 20):
            URL = self.BASE_URL.format(page)
            self.scrapePage(URL, page)    
            self.start_index = 0

    def scrapePage(self, url, page):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')

        WEBDRIVER_LOCATION = os.environ.get("WEBDRIVER_LOCATION")
        driver = webdriver.Chrome(WEBDRIVER_LOCATION, chrome_options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        urls = soup.find_all('a', class_ =  '_3DU-x JoRLr _3dYeW')
        titles = list(map(lambda element : element.contents[0] ,urls)) 
        urls = list(map(lambda element : element['href'], urls))
        self.scrapeTabs(urls[1], titles[1])
        for i in range(self.start_index,len(urls)):
            log.debug("scraping page : {} pos : {}".format(page, i))
            try:
                self.scrapeTabs(urls[i], titles[i])
            except:
                log.warning("failed scraping page : {} pos : {}".format(page, i))
        

    def scrapeTabs(self, url, title):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver", chrome_options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        text = soup.find('pre', class_ = '_3F2CP _3hukP')
        data = self.getText(text,soup)

        info = soup.find_all('div', class_ = '_3naMH')
        info_data = ['', '', '']
        for i in range(min(len(info),3)):
            if(len(info[i].find_all('a')) == 0):
                info_data[i] = info[i].contents[0]
        info1 = info_data[0]
        info2 = info_data[1]
        info3 = info_data[2]
        artist = soup.find('a', class_ = '_3DU-x _2LdY7').contents[0]
        self.db.addSong(title, artist, info1, info2, info3, data)        

    def getText(self, soup,ss):
        adding = False
        s = ""
        for span in soup.select('span._3PpPJ'):
            tag = ss.new_tag('tag')
            tag.string = span['data-name']
            for child in list(span.children):
                child.extract()
            span.insert_after(tag)
            span.unwrap()
        for child in soup.find_all('span', recursive = False):
            if(not adding):
                if(child['class'][0] == '_3rlxz'):
                    if ((child.contents[0])[0] == '['):
                        s = s + child.contents[0]
                        adding = True
            else:
                if(child['class'][0] == '_3rlxz'):
                    if(len(child.find_all('tag', recursive = False)) == 0):
                        if(not child.contents[0].isspace()):
                            s = s + child.contents[0]
                    else:
                        for tab in child.contents:
                            s = s + str(tab)

                else:
                    s = s + self.merge(child)
        
        return s
    
    
    def merge(self, soup):
        tags = soup.contents[0].contents
        lyrics = soup.contents[1].contents[0]
        s = ""
        lyrics_ptr = 0

        for tag in tags:
            if (str(tag)[0] == '<'):
                s = s + str(tag)
            else:
                s = s + lyrics[lyrics_ptr : min(lyrics_ptr + len(tag), len(lyrics))]
                lyrics_ptr = lyrics_ptr + len(tag)
        if(lyrics_ptr < len(lyrics)):
            s = s + lyrics[lyrics_ptr:]
        return s

        

