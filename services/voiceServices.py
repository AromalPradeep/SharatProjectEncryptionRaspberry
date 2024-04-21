import speech_recognition as sr

def listen():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        # Listen for the first phrase and extract the audio data
        audio = r.listen(source)
    
    try:
        print("trying")
        # Use Google Speech Recognition to convert the speech into text
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        # Error handling for unknown words
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        # Error handling for requests to the service
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return ""