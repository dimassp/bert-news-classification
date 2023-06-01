import requests
import pandas as pd
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
while True:
    pass