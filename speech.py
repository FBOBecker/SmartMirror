import speech_recognition as sr

r = sr.Recognizer()


def speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        print("i listened")
    try:
        print("letting google do its magic")
        msg = r.recognize_google(audio)
    except sr.UnknownValueError:
        msg = "Unknown Value Error"
        return msg
    except sr.RequestError:
        msg = "Request Error"
        return msg
    print("You said '" + msg + "'")
    return msg


def write():
    print("Watiting for you to type what you want.")
    return input()
