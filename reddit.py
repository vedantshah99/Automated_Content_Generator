from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import praw
import os
from time import sleep
from collections import namedtuple
from utility import getTitle, textToSpeech
import json

RedditPost = namedtuple("RedditPost", ["title", "url", "id", "comments"])
Comment = namedtuple("Comment", ["text", "id","url"])

#### Set up PRAW
r = praw.Reddit(
        client_id = "CMiWd6CGB6lF8-h7W3nKEA",
        client_secret = 'x0dkH-0W89qvbOQPXri2UnFUUZolEQ',
        user_agent = "Scraper 1.0 by /u/vedant"
    )

opts = FirefoxOptions()
s = Service('chromedriver/geckodriver')
opts.add_argument("--headless")
opts.set_preference("dom.push.enabled", False)  # kill notification popup
driver = Firefox(service=s, options=opts)
timeout = 10

#### Login Utility Function
def login():
    driver.get("https://www.reddit.com/login")
    user = driver.find_element(By.ID, "loginUsername")
    user.send_keys("DavidBrent9999")
    pwd = driver.find_element(By.ID, "loginPassword")
    pwd.send_keys("randomcheese9")
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    btn.click()
    sleep(timeout)
    try:
        cookie = driver.find_element(By.XPATH, '//button[text()="Accept all"]')
        cookie.click()  # kill cookie agreement popup. Probably not needed now'
    except NoSuchElementException:
        print('cookie not needed')

    sleep(timeout)


def praw_script(subreddit_name, number_of_posts, number_of_comments, full_path):
    login()
    ids = []

    for post in r.subreddit(subreddit_name).top(time_filter = 'month', limit=number_of_posts):
        postObj = {'id':post.id, 'title':getTitle(post.title), 'comments':[]}

        #### find the html area of the post title
        driver.set_window_size(400, 880)
        driver.get(post.url)
        title_html = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, f"t3_{post.id}")))

        #### create a folder for all media for current post 
        path = f"{full_path}\\{post.id}"
        if not os.path.isdir(path):
            os.mkdir(path)

        #### take screenshot of post title
        title_html.screenshot(f"{path}\\{post.id}.png")

        #### generate audio for post title
        textToSpeech(post.title, path, post.id)

        #### get url for all screenshots
        cmts = "https://www.reddit.com" + post.permalink
        driver.get(cmts)

        commentCount = 0
        i = 0
        comments_folder_path = f"{path}\\{post.id}_screenshots"
        if not os.path.isdir(comments_folder_path):
            os.mkdir(comments_folder_path)

        while commentCount < number_of_comments:
            comment = post.comments[i]
            i+=1

            if comment.author == 'AutoModerator':
                continue

            try:
                cmt = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, f"t1_{comment.id}")))
            except TimeoutException:
                print("Page load timed out...")
            else:
                commentCount+=1
                cmt.screenshot(f"{comments_folder_path}\\{comment.id}.png")
                textToSpeech(comment.body, comments_folder_path, comment.id)
                postObj['comments'].append(comment.id)
        
        with open(f'{path}\\{post.id}.txt', 'w') as json_file:
            json.dump(postObj, json_file)
        ids.append(post.id)
    return ids

############################################################################################



if __name__ == '__main__':
    list_of_posts = praw_script('askreddit',1,4, "C:\\Users\\vedan\\OneDrive\\Documents\\Python\\Automated_Content_Generator")
 