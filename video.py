from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, concatenate_audioclips, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.all import crop

import json


def generate_video(postId):
    print("GENERATING VIDEO")
    curTime = 0.0

    #### Title

    redditTitleAudio = AudioFileClip(f"{postId}\\{postId}.mp3")
    redditTitleImage = ImageClip(f"{postId}\\{postId}.png").set_start(curTime).set_duration(redditTitleAudio.duration).set_pos(("center", "center"))
    redditTitleImage = resize(redditTitleImage, 1)

    finalAudio = redditTitleAudio
    finalVideo = redditTitleImage

    curTime += redditTitleAudio.duration

    with open(f'{postId}\\{postId}.txt', 'r') as f:
        post = json.load(f)

    for comment in post['comments']:
        commentAudio = AudioFileClip(f"{postId}\{postId}_screenshots\{comment}.mp3")
        commentTextImage = ImageClip(f"{postId}\{postId}_screenshots\{comment}.png").set_start(curTime).set_duration(commentAudio.duration).set_pos(("center", "center"))
        commentTextImage = resize(commentTextImage, 1)

        curTime += commentAudio.duration

        finalAudio = concatenate_audioclips([finalAudio, commentAudio])
        finalVideo = concatenate_videoclips([finalVideo, commentTextImage])

    minecraftVideo = VideoFileClip("media\\Over an Hour of clean Minecraft Parkour (No Falls Full Daytime Download in description).mp4").subclip(30,30+finalAudio.duration)
    minecraftVideo.audioaudio = None

    final = CompositeVideoClip([minecraftVideo, finalVideo.set_position('center', 'center')])
    final.audio = finalAudio
    
    
    (w, h) = final.size

    crop_width = h * 9/16

    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    final = crop(final, x1=x1, y1=y1, x2=x2, y2=y2)

    final.write_videofile(f"final_videos\\{postId}.mp4")