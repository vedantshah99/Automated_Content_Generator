from reddit import praw_script
from video import generate_video


if __name__ == '__main__':
    postIds = praw_script('askreddit',1,4, "C:\\Users\\vedan\\OneDrive\\Documents\\Python\\Automated_Content_Generator")
    
    #postIds = ['15dbzoq']
    for postId in postIds:
        generate_video(postId)