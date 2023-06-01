# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# from pprint import pprint
# import json

# usernames = ["jlo","shakira","beyonce","katyperry"]
# PROXY= "11.456.448.110:8080"
# output = {}

# def main():
#     for username in usernames:
#         scrape(username)

# def prepare_browser():
#     edge_option = webdriver.EdgeOptions()
#     edge_option.add_argument(f'--proxy-server={PROXY}')
#     edge_option.add_argument('start-maximized')
#     edge_option.add_experimental_option('excludeSwitches',['enable-automation'])
#     edge_option.add_experimental_option('useAutomationExtension', False)
#     driver = webdriver.Edge(options=edge_option)
#     stealth(driver,
#             user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
#             languages= ["en-US", "en"],
#             vendor=  "Google Inc.",
#             platform=  "Win32",
#             webgl_vendor=  "Intel Inc.",
#             renderer=  "Intel Iris OpenGL Engine",
#             fix_hairline= False,
#             run_on_insecure_origins= False,
#             )
#     return driver

# def scrape(username): 
#     url = f'https://instagram.com/{username}/?__a=1&__d=dis'
#     edge = prepare_browser()
#     edge.get(url)
#     print (f"Attempting: {edge.current_url}")
#     if "login" in edge.current_url:
#         print ("Failed/ redir to login")
#         edge.quit()
#     else:
#         print ("Success")
#         resp_body = edge.find_element(By.TAG_NAME, "body").text
#         data_json = json.loads(resp_body)
#         user_data = data_json['graphql']['user']
#         parse_data(username, user_data)
#         edge.quit()

# def parse_data(username, user_data):
#     captions = []
#     if len(user_data['edge_owner_to_timeline_media']['edges']) > 0:
#         for node in user_data['edge_owner_to_timeline_media']['edges']:
#             if len(node['node']['edge_media_to_caption']['edges']) > 0:
#                 if node['node']['edge_media_to_caption']['edges'][0]['node']['text']:
#                     captions.append(
#                         node['node']['edge_media_to_caption']['edges'][0]['node']['text']
#                     )
#     output[username] = {
#         'name': user_data['full_name'],
#         'category': user_data['category_name'],
#         'followers': user_data['edge_followed_by']['count'],
#         'posts': captions,
#     }
# if __name__ == "__main__":
#     main()
#     pprint(output)

# import requests, json, random
# from pprint import pprint
# usernames = ["jlo", "shakira", "beyonce", "katyperry"]
# proxy = "http://11.456.448.110:8080"
# output = {}
# def get_headers(username):
#     headers = {
#         "authority": "www.instagram.com",
#         "method": "GET",
#         "path": "/{0}/".format(username),
#         "scheme": "https",
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "accept-encoding" : "gzip, deflate, br",
#         "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
#         "upgrade-insecure-requests": "1",
#         "Connection": "close",
#         "user-agent" : random.choice([
#               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
#               "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
#               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
#               "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
#             ])
#     }
#     return headers
# def parse_data(username, user_data):
#     captions = []
#     if len(user_data['edge_owner_to_timeline_media']['edges']) > 0:
#         for node in user_data['edge_owner_to_timeline_media']['edges']:
#             if len(node['node']['edge_media_to_caption']['edges']) > 0:
#                 if node['node']['edge_media_to_caption']['edges'][0]['node']['text']:
#                     captions.append(
#                         node['node']['edge_media_to_caption']['edges'][0]['node']['text']
#                     )
#     output[username] = {
#         'name': user_data['full_name'],
#         'category': user_data['category_name'],
#         'followers': user_data['edge_followed_by']['count'],
#         'posts': captions,
#     }
    
# def main():
#     for username in usernames:
#         url = f"https://instagram.com/{username}/?__a=1&__d=dis"    
#         response = requests.get(url, headers=get_headers(username), proxies = {'http': proxy, 'https': proxy})
#         if response.status_code == 200:
#             try:
#                 resp_json = json.loads(response.text)
#             except:
#                 print ("Failed. Response not JSON")
#                 continue
#             else:
#                 user_data = resp_json['graphql']['user']
#                 parse_data(username, user_data)
#         elif response.status_code == 301 or response.status_code == 302:
#             print ("Failed. Redirected to login")
#         else:
#             print("Request failed. Status: " + str(response.status_code))
# if __name__ == '__main__':
#     main()
#     pprint(output)
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
# from selenium.common.exceptions import NoSuchElementException
import pickle
edge_options = Options()
# edge_options.add_argument("--log-level=3")
# options.headless = True
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
# username = driver.find_element_by_name('username')
# username = driver.find_element(By.XPATH, '//input[@name="username"]')
# username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
# notNowButton = WebDriverWait(driver, 15).until(lambda d: d.find_element('xpath','//button[text()="Not Now"]'))
# notNowButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_acan _acao _acas _aj1-']")))
# notNowButton.click()
# notNowButon = driver.
# print("clicking not now button")
# notNowButton .click()
# print("not now button clicked")
# WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button']"))).click()
# WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button']"))).click()
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, "//*[local-name() = 'svg' and @aria-label='Search']"))).click()
keyword = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, "//*[local-name() = 'input' and @aria-label='Search input']")))
keyword.clear()
keyword.send_keys("sekitarbandungcom")
sekitarbandung = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, "//*[local-name() = 'span' and @class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj' and contains(string(), 'sekitarbandungcom')]")))
sekitarbandung.click()
time.sleep(5)
# posts = driver.find_elements(By.XPATH,"//div[@class='_aagv']")
last_height = driver.execute_script("return document.body.scrollHeight")
last =30
# while True:
# for i in range(0,last):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     counter = 1
#     # Wait to load the page.
#     time.sleep(2.5)

#     # Calculate new scroll height and compare with last scroll height.
#     new_height = driver.execute_script("return document.body.scrollHeight")

#     if new_height == last_height:
#         break
#     last_height = new_height
    
# for i in range(0,last):
#     print("scrolling...")
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     counter = 1
#     # Wait to load the page.
#     time.sleep(2)

#     # Calculate new scroll height and compare with last scroll height.
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height



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
        # time.sleep(2)
        
        # time.sleep(3)
    # for caption in current_captions:
    #     if caption in captions:
    #         print("post already in list, skipped")
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(2)
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #         print(f'last height: {last_height}\nnew height: {new_height}')
    #         if new_height == last_height:
    #             print("last height equals new height, stop scrolling")
    #             break
    #         last_height = new_height
    #         time.sleep(3)
    #     else:
    #         print(f"caption: \n{caption}")
    #         print("Adding post to a list...")
    #         captions.append(caption)
    #         print("caption added to list")
    #         time.sleep(3)
    # print("scrolling...")
    # counter = 1
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the page.
    
    # time.sleep(2)

    # new_height = driver.execute_script("return document.body.scrollHeight")
    # # Calculate new scroll height and compare with last scroll height.
    # if new_height == last_height:
    #     break
    # last_height = new_height
    # print(f'last height: {last_height}\nnew height: {new_height}')
    
# posts = driver.find_elements(By.XPATH,"//article//a[@role='link']")
# print("total posts: {}".format(len(posts)))
# for i, post in enumerate(posts):
#     print(f"post number {i+1}")
#     time.sleep(2)
#     try:
#         print('clicking post')
#         post.click()
#         time.sleep(2)
#         caption = driver.find_element(By.XPATH,"//div[@class='_a9zs']").text
#         ac.move_by_offset(0,0).click().perform()
#         counter +=1
#     except (StaleElementReferenceException, NoSuchElementException) as e:
#         print("Print error")
#         print(e)
#         time.sleep(2)
#         continue
while True:
    pass