from datetime import datetime
import pyscreenshot as ImageGrab
from collections import namedtuple
import praw
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

firefox_options = Firefox_Options()
s = Service('chromedriver/geckodriver')


RedditPost = namedtuple("RedditPost", ["title", "url", "id", "comments"])
Comment = namedtuple("Comment", ["text", "id","url"])

def main():
    list_of_posts = praw_script('askreddit',1,4)
    take_screenshot(list_of_posts)

def take_screenshot(posts):
    print("COLLECTING SCREENHOTS\n")
    for post in posts:
        uneditedTitle = "_".join(post.title.split(" "))
        title = ""
        for c in uneditedTitle:
            if c not in "?*\"\'":
                title+=(c)
        del uneditedTitle

        driver = webdriver.Firefox(service=s, options=firefox_options)
        driver.get(post.url)
        
        title_html = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[@id=\"t3_{post.id}\"]")))

        path = f"C:\\Users\\vedan\\OneDrive\\Documents\\Python\\Automated_Content_Generator\\{title}"

        if not os.path.isdir(path):
            os.mkdir(path)

        title_html.screenshot(f"{path}\\{post.id}.png")
        driver.close()

        
        comments_folder_path = f"{path}\\{post.id}_screenshots"

        if not os.path.isdir(comments_folder_path):
            os.mkdir(comments_folder_path)
        
        for comment in post.comments:
            driver = webdriver.Firefox(service=s, options=firefox_options)
            driver.get(comment.url)

            

            comment_html = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[@id=\"t1_{comment.id}-comment-rtjson-content\"]")))
            
            try:
                comment_html.screenshot(f"{comments_folder_path}\\{comment.id}.png")
            except:
                print(f"Error with {comment.id}")

            driver.close()



#### Inputs : Name of Subreddit, Number of posts to collect, Number of comments to collect within each post
#### Returns : List of Posts
def praw_script(subreddit_name, number_of_posts, number_of_comments):
    print("PARSING REDDIT\n")

    #### setting up praw
    user_agent = "Scraper 1.0 by /u/vedant"
    reddit = praw.Reddit(
        client_id = "CMiWd6CGB6lF8-h7W3nKEA",
        client_secret = 'x0dkH-0W89qvbOQPXri2UnFUUZolEQ',
        user_agent = user_agent
    )

    posts = []

    #### iterates through top posts of the month within subreddit
    for post in reddit.subreddit(subreddit_name).top(time_filter = 'month', limit=number_of_posts):
        #print(post.title)
        #print(post.url,"\n")

        comment_list = []

        #### iterates through comment section
        for comment in post.comments.list()[:number_of_comments]:
            comment_url = f"https://www.reddit.com/r/{post.subreddit.display_name}/comments/{post.id}/comment/{comment.id}/?utm_source=reddit&utm_medium=web2x&context=3"
            print(comment_url)
            print(comment.body,"\n")

            #### creates comment object with attributes of (comment text and comment url)
            comment_list.append(Comment(comment.body,comment.id, comment_url))
        
        #### creates list of posts with attributes (post title, post url, list of top comments from post)
        posts.append(RedditPost(post.title, post.url, post.id, comment_list))
    
    print(posts)
    return posts
            



if __name__ == '__main__':
    "Grab the whole screen"
    import pyscreenshot as ImageGrab

    main()