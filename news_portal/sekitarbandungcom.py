import time
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
from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd
df = pd.DataFrame()
edge_options = Options()
edge_options.add_argument("--log-level=3")
# options.headless = True
driver = webdriver.Edge("D:\PROGRAMMING\python\bert_news_type_and_topic_classification\msedgedriver.exe",options=edge_options)
driver.get("https://www.sekitarbandung.com/category/jawa-barat/")
main = driver.find_element(By.XPATH,"//button[contains(text(), 'SEACRH')]")
# print("Hello world")
time.sleep(3)
driver.execute_script("arguments[0].scrollIntoView(true);", main);
time.sleep(5)
driver.execute_script("window.scrollBy(0,-300);", main) 
try:
    # load_posts = driver.find_element(By.XPATH,"//div[contains(text(), 'Load More Posts')]")

    load_posts = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH,"//div[contains(text(), 'Load More Posts')]")))
    print("Load more posts...")
    driver.execute_script("arguments[0].scrollIntoView(true);", load_posts);
except StaleElementReferenceException:
    pass
time.sleep(15)
article_elements = WebDriverWait(driver, 500).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='post-content']//h2//a")))
print(f"total articles: {len(article_elements)}")
articles = []
for i, article in enumerate(article_elements):
    _a = BeautifulSoup(article.get_attribute('outerHTML'),'html5lib')
    href = _a.find('a')
    link = href['href']
    news = requests.get(link)
    news_page = BeautifulSoup(news.content,'html5lib')
    post_content = news_page.find('div', {'class': 'post-content'})
    print(f'content number: {i+1}')
    # time.sleep(1.5)
    print('text: ')
    # time.sleep(3)
    print(post_content.text.replace('\n',''))
    articles.append(post_content.text.replace('\n',''))
df = pd.DataFrame(articles, columns=["news"])
df.to_csv('sekitarbandungcom.csv', index=False)
while True:
    pass