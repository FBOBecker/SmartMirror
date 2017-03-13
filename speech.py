import speech_recognition as sr

r = sr.Recognizer()


def speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        msg = r.recognize_google(audio)
    except sr.UnknownValueError:
        msg = "Unknown Value Error"
    except sr.RequestError:
        msg = "Request Error"
    return msg
