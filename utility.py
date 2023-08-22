import pyttsx3

def remove_profanity(text):
    translate = {'fuck':'fork', 'fucking':'ducking', 'shit':'ship', 'bitch':'lady'}

    res = ""
    for word in text.split(' '):
        if word.lower() in translate:
            res += translate[word.lower()]
        else:
            res += word
        res += " "
    return res[:-1]

def getTitle(origTitle):
    uneditedTitle = "_".join(origTitle.split(" "))
    title = ""
    for c in uneditedTitle:
        if c not in "?*\"\'":
            title+=(c)
    del uneditedTitle
    return title


def textToSpeech(text, path, id):
    text = remove_profanity(text)
    engine = pyttsx3.init()
    engine.save_to_file(text , f"{path}\\{id}.mp3")
    engine.runAndWait()