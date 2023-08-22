import praw
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyttsx3
from collections import namedtuple

from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, concatenate_audioclips, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.all import crop

from utility import remove_profanity, getTitle
from reddit import praw_script

firefox_options = Firefox_Options()
s = Service('chromedriver/geckodriver')


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

        comment_list = []

        #### iterates through comment section
        for comment in post.comments.list()[:number_of_comments]:
            comment_url = f"https://www.reddit.com/r/{post.subreddit.display_name}/comments/{post.id}/comment/{comment.id}/?utm_source=reddit&utm_medium=web2x&context=3"

            #### creates comment object with attributes of (comment text and comment url)
            comment_list.append(Comment(comment.body,comment.id, comment_url))
        
        #### creates list of posts with attributes (post title, post url, list of top comments from post)
        posts.append(RedditPost(post.title, post.url, post.id, comment_list))

    return posts

def collect_screenshots_and_audio_files(posts):
    print("COLLECTING SCREENHOTS\n")

    for post in posts:

        #### remove spaces and punctuation from post title
        title = getTitle(post.title)

        #### open the driver
        driver = webdriver.Firefox(service=s, options=firefox_options)
        driver.set_window_size(400, 880)
        driver.get(post.url)

        #### find the html area of the post title
        title_html = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, f"t3_{post.id}")))

        #### create a folder for all media for current post 
        path = f"C:\\Users\\vedan\\OneDrive\\Documents\\Python\\Automated_Content_Generator\\{title}"
        if not os.path.isdir(path):
            os.mkdir(path)

        #### take screenshot of post title
        title_html.screenshot(f"{path}\\{post.id}.png")
        #driver.close()

        #### generate the text-to-speech file of the post title
        textToSpeech(post.title, path, post.id)
        

        #### COMMENTS
        #### create folder within post file to store all comments-related media
        comments_folder_path = f"{path}\\{post.id}_screenshots"
        if not os.path.isdir(comments_folder_path):
            os.mkdir(comments_folder_path)
        
        for comment in post.comments:
            # open driver
            driver.set_window_size(1200, 880)
            driver.get(comment.url)

            # close_buttom = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id=\"secondary-button\"]")))
            # close_buttom.click()
            # driver.set_window_size(400, 880)

            # sometimes the comment isn't automatically open (will fix eventually)
            try:
                # find corrent html area to screenshot
                comment_html = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[@id=\"t1_{comment.id}-comment-rtjson-content\"]")))

                comment_html.screenshot(f"{comments_folder_path}\\{comment.id}.png")
                textToSpeech(comment.text, comments_folder_path, comment.id)
            except:
                print(f"Error with {comment.id}")

        driver.close()

def generate_video(posts):
    print("GENERATING VIDEO")

    for post in posts:
        curTime = 0.0

        #### Title
        title = getTitle(post.title)

        redditTitleAudio = AudioFileClip(f"{title}\\{post.id}.mp3")
        redditTitleImage = ImageClip(f"{title}\\{post.id}.png").set_start(curTime).set_duration(redditTitleAudio.duration).set_pos(("center", "center"))
        redditTitleImage = resize(redditTitleImage, 0.7)

        finalAudio = redditTitleAudio
        finalVideo = redditTitleImage

        curTime += redditTitleAudio.duration

        for comment in post.comments:
            if not os.path.isfile(f"{title}\{post.id}_screenshots\{comment.id}.mp3"):
                continue

            commentAudio = AudioFileClip(f"{title}\{post.id}_screenshots\{comment.id}.mp3")
            commentTextImage = ImageClip(f"{title}\{post.id}_screenshots\{comment.id}.png").set_start(curTime).set_duration(commentAudio.duration).set_pos(("center", "center"))
            commentTextImage = resize(commentTextImage, 0.7)

            curTime += commentAudio.duration

            finalAudio = concatenate_audioclips([finalAudio, commentAudio])
            finalVideo = concatenate_videoclips([finalVideo, commentTextImage])

        minecraftVideo = VideoFileClip("Over an Hour of clean Minecraft Parkour (No Falls Full Daytime Download in description).mp4").subclip(30,30+finalAudio.duration)
        minecraftVideo.audioaudio = None

        final = CompositeVideoClip([minecraftVideo, finalVideo.set_position('center', 'center')])
        final.audio = finalAudio
        
        
        (w, h) = final.size

        crop_width = h * 9/16

        x1, x2 = (w - crop_width)//2, (w+crop_width)//2
        y1, y2 = 0, h
        final = crop(final, x1=x1, y1=y1, x2=x2, y2=y2)

        final.write_videofile(f"final_videos\\{post.id}.mp4")
        #if not os.path.isfile(f"final_videos\\{post.id}.mp4"):
            #final.write_videofile(f"final_videos\\{post.id}.mp4")


if __name__ == '__main__':
    praw_script('askreddit',1,4, "C:\\Users\\vedan\\OneDrive\\Documents\\Python\\Automated_Content_Generator")
    #generate_video(list_of_posts)