from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from datetime import date
from bs4 import BeautifulSoup
from transformers import pipeline
import pandas as pd
import requests
import datetime
import time
import re
import time

clf = pipeline(model="dimassamid/IndobertNewsTest")
type_clf = pipeline(model="rizalmilyardi/IndobertTypeNews")

class Scrape():
    def __init__(self):
        # print(f"news portals: {self.news_portals}")
        self.scrape_functions = {
            "detiknewsjabar" : self.__detik,
            "antaranewsjabar" : self.__jabarantaranews,
            "prbandung" : self.__prbandung,
            "sekitarbandung" : self.__sekitarbandung
        }
        self.articles = []
        pass    
    
    def scrape_news(self, news_portals: list, start_date=str(date.today()), end_date=str(date.today())):
        """
        Return news that's scraped from selected portal with specificied time
        
        Parameters
        ------------
        news_portals:
                    Available news portals: 
                    Detik News Jabar\t: detiknewsjabar
                    Antara News Jabar\t: antaranewsjabar
                    Pikiran Rakyat Bandung\t: prbandung
                    Sekitar Bandung\t: sekitarbandung
                    Tribun Jabar\t: tribunjabar
        start_date:
                    input start date with format: "yyyy-mm-dd"
                    example: 2023-08-23
        end_date:
                    input end date with format-> "yyyy-mm-dd"
                    example: 2023-10-1
        Returns
        ------------
        articles:
                 contains list of dictionaries that's store the id of news and news itself
                 example return: [
                     {
                         id  : "detik.com/news-1"
                         news: "some news text"
                     },
                     {
                         id  : "detik.com/news-2"
                         news: "some news text"
                     },
                ]
        """
        self.news_portals = news_portals
        self.start_date = start_date
        self.end_date = end_date
        # print(f"hello world from scrape news")
        # print(f"news portals {self.news_portals }")
        # print(f"start date {self.start_date}")
        # print(f"end date {self.end_date}")
        for portal in self.news_portals:
            print(f'portal: {portal}')
            self.scrape_functions[portal]()
        return self.articles
        # pass
    def get_scraped_news(self):
        """
        Returns
        ------------
        articles:
                list of dictionaries that contain news id and scraped news 
        """
        return self.articles
    # def convert_mon(self, month, portal_id):
    def convert_mon(self, month):
        # print(f"old month: {month}")
        months = {
            "01" : ["Jan", "January", "Januari"],
            "02" : ["Feb", "February", "Februari"],
            "03" : ["Mar", "March", "Maret"],
            "04" : ["Apr", "April"],
            "05" : ["May", "Mei"],
            "06" : ["Jun", "June", "Juni"],
            "07" : ["Jul", "July", "Juli"],
            "08" : ["Aug", "Agu", "August","Agustus"],
            "09" : ["Sep", "September"],
            "10" : ["Oct"," Okt", "October","Oktober"],
            "11" : ["Nov"," November","Nopember"],
            "12" : ["Dec"," Des", "December","Desember"],
        }
        for key, value in months.items():
            if type(month) is not str:
                if month.group(1) in value:
                    month = key
                    break
            else:
                if month in value:
                    month = key
                    break
                
                
        # print(f"new month: {month}")
        return month
    def get_news_date(self, raw_date):
        """
        Return new news date format that will be converted from news date 
        
        Parameters
        ------------
        raw_date :
                    date that will be converted from format that's 
                    come from each news portal to a new date format.
                    Example:
                    original format: 12 March 2021
                    new format: 2021-03-12
                    or
                    original format: blablabla 12 March 2021 blablabla
                    new format: 2021-03-12
        Returns
        ------------
        news_date:
                    new news date format
        """
        news_date = re.search("([0-9]+\s[A-Za-z]+\s[0-9]+)", raw_date).group(1)
        # print(f"news date from get news date: {news_date}")
        news_date = re.sub(r"([A-Za-z]+)",  self.convert_mon, news_date)
        news_date = news_date.split(" ")
        news_date.reverse()
        news_date = "-".join(news_date)
        # print("news_date from function get news date: {}".format(news_date))
        # time.sleep(10)
        return news_date
    def __detik(self):
        loopable = True
        page = 1
        print("Hello world from detik news jabar")
        while loopable:
            print(f"page {page}")
            url = f"https://www.detik.com/tag/jawa-barat/?sortby=time&page={page}"
            request = requests.get(url)
            articles_page = BeautifulSoup(request.content,"html5lib")
            # print(type(articles_page))
            
            for i, article in enumerate(articles_page.find_all("article")):
                get_date = article.find("span",{"class":{"date"}})
                news_date = self.get_news_date(get_date.contents[1])
                print("Hello world from for loop")
                # date_now = datetime.datetime.today().strftime('%Y-%m-%d')
                if news_date > self.end_date:
                    print("News date bigger than end date, skipped.")
                    continue
                if news_date >= self.start_date and news_date <= self.end_date:
                    print(f"article {i+1}")
                    news_link = article.find("a")
                    get_news = requests.get(news_link['href'])
                    # print(f"news link: {news_link['href']}")
                    # news_id = re.search("https?://www.([\w\-]+(\.[\w\-]+)+\S*)", news_link['href']).group(1)
                    find_id = re.search("https?://www.([\w\-]+(\.[\w\-]+)+\S*)", news_link['href'])
                    if find_id:
                        news_id = find_id.group(1)
                    else:
                        news_id = news_link['href']
                    news_html = BeautifulSoup(get_news.content,"html5lib")
                    print("Hello world form line after news_html")
                    if news_html.find("div", {"class": {"paradetail"}}) is not None:
                        pass
                        news_html.find("div", {"class": {"paradetail"}}).decompose()
                        text = news_html.find("div",{"class":{"detail__body-text"}})
                        full_text = ""
                        for p in text.find_all("p"):
                            # print(p.text.strip())
                            full_text += p.text.strip()
                        print(full_text)
                        # self.articles.append({
                        #     "id": news_id,
                        #     "news": full_text
                        # })
                        self.classify_news(full_text[:255])
                        self.articles.append((news_id, full_text, news_link['href']))
                else:
                    # print("That's it")
                    loopable = False
                    break
            page +=1
        # return self.articles
    def __jabarantaranews(self):
        loopable = True
        page = 1
        while loopable:
            print(f"page {page}")
            url = f"https://jabar.antaranews.com/terkini/{page}"
            request = requests.get(url)
            articles_page = BeautifulSoup(request.content,"html5lib")
            article_block = articles_page.find("div",{"class":{"col-md-8"}})
            for i, article in enumerate(article_block.find_all("article")):
                get_date = article.find("p",{"class":{"simple-share"}})                
                news_date = re.search("(jam\slalu|menit\slalu|detik\slalu)",get_date.text)
                if news_date:
                    # print("news date equals today")
                    news_date = datetime.datetime.today().strftime('%Y-%m-%d')
                else:
                    # print("news is not today")
                    
                    news_date = self.get_news_date(get_date.text)
                # print(f"news date: {news_date}")
                if news_date > self.end_date:
                    # print("News date bigger than end date, skipped.")
                    continue
                if news_date >= self.start_date and news_date <= self.end_date:
                    # print(f"article {i+1}")
                    news_link = article.find("a")
                    get_news = requests.get(f"{news_link['href']}?page=all")
                    # print(f"news link: {news_link['href']}")
                    news_id = re.search("https?://[A-Za-z0-9]+.([\w\-]+(\.[\w\-]+)+\S*)", news_link['href']).group(1)
                    news_html = BeautifulSoup(get_news.content,"html5lib")
                    text = news_html.find("div", {"class": {"post-content"}})
                    # print(text.text)
                    # self.articles.append({
                    #     "id": news_id,
                    #     "news": text.text
                    # })
                    if text is not None:
                        self.classify_news(text.text[:255])
                        self.articles.append((news_id, text.text, news_link['href']))
                else:
                    loopable =False
                    break
                if page >100:
                    loopable = False
                    break
            page +=1
    def __prbandung(self):
        loopable = True
        page = 1
        while loopable:
            print(f"page {page}")
            url = f"https://www.pikiran-rakyat.com/bandung-raya?page={page}"
            request = requests.get(url)
            articles_page = BeautifulSoup(request.content,"html5lib")
            # article_block = articles_page.find("div",{"class":{"col-md-8"}})
            for i, article in enumerate(articles_page.find_all('div', {'class': {'latest__item'}})):
                print(f"article {i+1}")
                get_date = article.find("date")
                news_date = re.search("(jam\slalu|menit\slalu|detik\slalu)",get_date.text)
                # if news_date:
                #     print("news date equals today")
                #     news_date = datetime.datetime.today().strftime('%Y-%m-%d')
                # else:
                news_date = self.get_news_date(get_date.text)
                # print(f"new news date: {news_date}")
                if news_date > self.end_date:
                    print("News date bigger than end date, skipped.")
                    continue
                if news_date >= self.start_date and news_date <= self.end_date:
                    news_link = article.find("a")
                    get_news = requests.get(f"{news_link['href']}?page=all")
                    # print(f"news link: {news_link['href']}")
                    news_id = re.search("https?://[A-Za-z0-9]+.([\w\-]+(\.[\w\-]+)+\S*)", news_link['href']).group(1)
                    news_html = BeautifulSoup(get_news.content,"html5lib")
                    text = news_html.find("article", {"class": {"read__content"}})
                    # print("text: ")
                    # print(text.text)
                    # time.sleep(1)
                    # self.articles.append({
                    #     "id": news_id,
                    #     "news": text.text.strip().replace(u'\xa0', u' ')
                    # })
                    # self.classify_news(text.text.strip().replace(u'\xa0', u' '))
                    self.classify_news(text.text.strip().replace(u'\xa0', u' ')[:255])
                    self.articles.append((
                        news_id,
                        text.text.strip().replace(u'\xa0', u' '),
                        news_link['href']))
                else:
                    loopable =False
                    break
                if page >10:
                    loopable = False
                    break
            page +=1
    def __sekitarbandung(self):
        
        df = pd.DataFrame()
        edge_options = Options()
        edge_options.add_argument("--log-level=3")
        # options.headless = True
        driver = webdriver.Edge("D:\PROGRAMMING\python\bert_news_type_and_topic_classification\msedgedriver.exe",options=edge_options)
        driver.get("https://www.sekitarbandung.com/category/jawa-barat/")
        try:
            wait = 1.5
            for i in range(0,5):
                # load_posts = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(text(), 'Load More Posts')]")))
                load_posts = driver.find_element(By.XPATH,"//a[contains(text(), 'Load More Posts')]")
                print(f"Load more posts... Wait {wait} seconds")
                driver.execute_script("arguments[0].click();", load_posts);
                time.sleep(wait)
        except StaleElementReferenceException:
            print("Stale Element Reference Exception thrown")
            pass
        article_elements = WebDriverWait(driver, 500).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='post-content']//h2//a[1]")))
        print(f"total articles: {len(article_elements)}")
        # articles = []
        for i, article in enumerate(article_elements):
            _a = BeautifulSoup(article.get_attribute('outerHTML'),'html5lib')
            href = _a.find('a')
            link = href['href']
            news = requests.get(link)
            news_id = re.search("https?://[A-Za-z0-9]+.([\w\-]+(\.[\w\-]+)+\S*)", href['href']).group(1)
            news_page = BeautifulSoup(news.content,'html5lib')
            post_content = news_page.find('div', {'class': 'entry-content'})
            texts = post_content.find_all('p')
            content = ''
            for text in texts:
                content += text.text
            print(f'content number: {i+1}')
            # time.sleep(1.5)
            print('text: ')
            # self.articles.append({
            #     "id": news_id,
            #     "news": content
            # })
            self.classify_news(content[:255])
            self.articles.append((news_id, content, href['href']))
            # print(post_content.text.replace('\n',''))
            # articles.append(post_content.text.replace('\n',''))
        # articles = []
        # for i, article in enumerate(article_elements):
        #     _a = BeautifulSoup(article.get_attribute('outerHTML'),'html5lib')
        #     href = _a.find('a')
        #     link = href['href']
        #     news = requests.get(link)
        #     news_page = BeautifulSoup(news.content,'html5lib')
        #     post_content = news_page.find('div', {'class': 'post-content'})
        #     print(f'content number: {i+1}')
        #     # time.sleep(1.5)
        #     print('text: ')
        #     # time.sleep(3)
        #     print(post_content.text.replace('\n',''))
        #     articles.append(post_content.text.replace('\n',''))
        # df = pd.DataFrame(articles, columns=["news"])
        # df.to_csv('sekitarbandungcom.csv', index=False)
        
    def instagram():
        edge_options = Options()
        driver = webdriver.Edge("D:\PROGRAMMING\python\bert_news_type_and_topic_classification\msedgedriver.exe",options=edge_options)
        # driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        driver.get("https://www.instagram.com")

        username = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        username.send_keys('msaid104')
        password.clear()
        password.send_keys('<4PacMan4>')
        Login_button = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        Login_button.click()
        ac = ActionChains(driver)
        WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, "//*[local-name() = 'svg' and @aria-label='Search']"))).click()
        keyword = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, "//*[local-name() = 'input' and @aria-label='Search input']")))
        keyword.clear()
        keyword.send_keys("sekitarbandungcom")
        sekitarbandung = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, "//*[local-name() = 'span' and @class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj' and contains(string(), 'sekitarbandungcom')]")))
        sekitarbandung.click()
        time.sleep(5)
        last_height = driver.execute_script("return document.body.scrollHeight")
        last =30
        captions = []
        while True:
            try:
                
                posts = driver.find_elements(By.XPATH,"//article//a[@role='link']")
                print(f"total posts: {len(posts)}")
                for i, post in enumerate(posts):
                    print(f"post {i+1} out of {len(posts)}")
                    post.click()
                    time.sleep(2)
                    caption = driver.find_element(By.XPATH,"//div[@class='_a9zs']").text
                    if caption not in captions:
                        print(f"caption: \n{caption}")
                        print("Adding post to a list...")
                        captions.append(caption)
                        print("caption added to list")
                        # time.sleep(3)
                        print("end")
                    else:
                        print("caption already in list, skipped. Continue scrolling")
                        ac.move_by_offset(0,0).click().perform()
                        break
                    ac.move_by_offset(0,0).click().perform()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                new_height = driver.execute_script("return document.body.scrollHeight")
                print(f'last height: {last_height}\nnew height: {new_height}')
                if new_height == last_height:
                    print("last height equals new height, stop scrolling")
                    break
                last_height = new_height
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                # print("Element intercepted, waiting for 2 secs")
                print("An error occured, scrolling post")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                new_height = driver.execute_script("return document.body.scrollHeight")
                print(f'last height: {last_height}\nnew height: {new_height}')
                if new_height == last_height:
                    print("last height equals new height, stop scrolling")
                    break
                last_height = new_height
                pass
    def classify_news(self, news):
        news_type = type_clf(news)[0]['label']
        if news_type != 'non-kejadian':
            news_topic =clf(news)[0]['label']
        else :
            news_topic = '-'
        print(f"news type: {news_type}")
        print(f"news topic: {news_topic}")
# s = Scrape()
# s.scrape_news(['detiknewsjabar'])
# articles = s.get_scraped_news()