import pyautogui                        # Automate keyboard/mouse actions
import time                             # Handle delays
import speech_recognition as sr         # Speech recognition
import pyttsx3                          # Text-to-speech
import datetime                         # Get date and time
import re                               # Regular expressions for text processing
import os                               # File operations
import webbrowser                       # Open web pages
import yt_dlp                           # Download YouTube videos
import requests                         # Handle HTTP requests
from googletrans import Translator      # Translate text

# Initialize components
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

# Function to speak the result
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice input
def listen():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        return audio

# Function to recognize speech and return the text
def recognize_speech(audio):
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Please repeat.")
        return None
    except sr.RequestError:
        speak("Sorry, I'm having trouble with the speech service. Try again later.")
        return None

# Time and Date Functions
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current time is: {current_time}")
    speak(f"The current time is {current_time}")

def tell_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %d %B %Y")
    print(f"Today's date is: {current_date}")
    speak(f"Today's date is {current_date}")

# Mathematical Calculation Functions
def parse_command(command):
    command = re.sub(r"(sum|add|plus) of", "+", command)
    command = re.sub(r"(raised to the|raised to|raise to the|raise to|power of)", "**", command)
    command = re.sub(r"(minus|subtract) from", "-", command)
    command = re.sub(r"(times|multiply by)", "*", command)
    command = re.sub(r"(divided by)", "/", command)
    command = re.sub(r'[^0-9+\-*/().^ ]', '', command)
    return command

def calculate(command):
    try:
        expression = parse_command(command)
        result = eval(expression)
        print(f"The result is: {result}")
        speak(f"The result is {result}")
    except Exception:
        speak("Sorry, I couldn't perform the calculation.")

# Open Application Function
def open_app(app_name):
    speak(f"Opening {app_name}.")
    pyautogui.hotkey('win', 's')
    time.sleep(1)
    pyautogui.write(app_name)
    time.sleep(1)
    pyautogui.press('enter')

# File Management Functions
def create_file(file_name, file_extension):
    try:
        with open(f"{file_name}.{file_extension}", 'w') as file:
            file.write("")
        speak(f"File {file_name}.{file_extension} created successfully.")
    except Exception:
        speak("Error occurred while creating the file.")

def rename_file(old_name, new_name, extension):
    try:
        os.rename(f"{old_name}.{extension}", f"{new_name}.{extension}")
        speak(f"File renamed to {new_name}.{extension}")
    except FileNotFoundError:
        speak("File not found.")

def delete_file(file_name, file_extension):
    try:
        os.remove(f"{file_name}.{file_extension}")
        speak(f"File {file_name}.{file_extension} deleted successfully.")
    except FileNotFoundError:
        speak("File not found.")

# Joke Function
def tell_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    if response.status_code == 200:
        joke_data = response.json()
        joke = joke_data.get("joke", f"{joke_data.get('setup')} ... {joke_data.get('delivery')}")
        speak(joke)
    else:
        speak("Sorry, I couldn't fetch a joke.")

# YouTube Song Player
def play_youtube_song(song_title):
    search_query = f"ytsearch:{song_title}"
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)
            if 'entries' in result and result['entries']:
                video = result['entries'][0]
                video_url = video['webpage_url']
                speak(f"Now playing {video['title']}")
                webbrowser.open(video_url)
    except Exception:
        speak("An error occurred while searching for the song.")

# Weather Function
def get_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    weather_data = response.text.strip()
    if weather_data:
        speak(f"The weather in {city} is {weather_data}")
    else:
        speak("Could not retrieve weather data.")

# Text Translation Function
def translate_text(text, target_language="en"):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Google Search Function
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

def main():
    speak("Hello!")

    while True:
        speak("Say a command or 'exit' to quit.")
        audio = listen()
        command = recognize_speech(audio)

        if command:
            if 'exit' in command:
                speak("Goodbye!")
                break
            elif 'time' in command and 'date' not in command:
                tell_time()
            elif 'date' in command and 'time' not in command:
                tell_date()
            elif 'time' in command and 'date' in command:
                tell_time()
                tell_date()    
            elif 'open' in command:
                app_name = command.replace("open", "").strip()
                open_app(app_name)
            elif 'calculate' in command:
                calculate(command)
            elif 'create file' in command:
                speak("What is the file name?")
                file_name = recognize_speech(listen())
                speak("What is the file extension?")
                file_extension = recognize_speech(listen())
                create_file(file_name, file_extension)
            elif 'rename file' in command:
                speak("What is the old file name?")
                old_name = recognize_speech(listen())
                speak("What is the new file name?")
                new_name = recognize_speech(listen())
                speak("What is the file extension?")
                extension = recognize_speech(listen())
                rename_file(old_name, new_name, extension)
            elif 'delete file' in command:
                speak("What is the file name?")
                file_name = recognize_speech(listen())
                speak("What is the file extension?")
                file_extension = recognize_speech(listen())
                delete_file(file_name, file_extension)
            elif 'joke' in command:
                tell_joke()
            elif 'play song' in command:
                speak("What song do you want to play?")
                song_title = recognize_speech(listen())
                play_youtube_song(song_title)
            elif 'weather' in command:
                speak("Which city's weather would you like to know?")
                city = recognize_speech(listen())
                get_weather(city)
            elif 'translate' in command:
                speak("What would you like to translate?")
                text = recognize_speech(listen())
                speak("Which language should I translate to?")
                language = recognize_speech(listen())
                translated_text = translate_text(text, language)
                speak(f"The translation is: {translated_text}")
            else:
                search_google(command)
        else:
            print("Sorry i couldnt understand the command")
            speak("Sorry i couldnt understand the command")

if __name__ == "__main__":
    main()
