import speech_recognition as sr
import pyttsx3 as tts
import pandas as pd
import re


def speech_to_text(recognizer, microphone):
    print('Listening...')
    audio = recognizer.listen(microphone, phrase_time_limit=3)
    text = recognizer.recognize_google(audio)
    text = text.lower()
    print(f"speech_to_text: {text}")
    return text


def map_to_response(text, patterns, responses):
    print('Thinking...')
    response = ''
    for index, pattern in enumerate(patterns):
        if re.search(pattern, text):
            response = responses[index]
            break
    print(f"map_to_response: {text}->{response}")
    return response


def text_to_speech(engine, text):
    print('Speaking...')
    engine.say(text)
    engine.runAndWait()
    print(f"text_to_speech: {text}")
    return 0


def main():
    df = pd.read_csv(filepath_or_buffer='phrase_map.csv', header=0)
    patterns = df['regex_pattern'].tolist()
    responses = df['response'].tolist()
    engine = tts.init()
    recognizer = sr.Recognizer()
    with sr.Microphone() as microphone:
        while True:
            try:
                text = speech_to_text(recognizer=recognizer, microphone=microphone)
                response = map_to_response(text=text, patterns=patterns, responses=responses)
                if response != '':
                    text_to_speech(engine=engine, text=response)
                    if response == 'goodbye!':
                        break
            except Exception as e:
                print(f"Error - {e}")
                continue


if __name__ == "__main__":
    main()
