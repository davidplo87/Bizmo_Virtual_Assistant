from __future__ import print_function
import datetime
import os.path
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
from playsound import playsound
import speech_recognition as sr
import pyttsx3
import pytz
from twilio.rest import Client
from googletrans import Translator
from gtts import gTTS
import gtts.lang

from config import SCOPES, MONTHS, DAYS, DAY_EXTENTIONS, CONTACTS, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

tr = Translator()
engine = pyttsx3.init()

# Creates 2 wake words.  
wake_words = ["bizmo", "bismo"]

#Takes a string and plays audio to the user.
def speak(text):
    engine.say(text)
    engine.runAndWait()

#Prints a string and plays audio at the same time       
def print_and_speak(string):
    print(string)
    speak(string)

#Listens for user audio. Returns the audio as a string. 
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:           
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()

#Function that calls the Google Calendar API and checks to see if the user has any upcoming events scheduled.
def get_events(date, service):     
        # Call the Calendar API
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(date, datetime.datetime.max.time())
        utc = pytz.UTC
        date = date.astimezone(utc)
        end_date = end_date.astimezone(utc)

        events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(), 
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print_and_speak('No upcoming events found.')
        else: 
            speak(f"You have {len(events)} events on this day.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                start_time = str(start.split("T")[1].split("-")[0])
                if int(start_time.split(":")[0]) < 12:
                    start_time = start_time + "am"
                else:
                    start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                    start_time = start_time + "pm"

                speak(event["summary"] + " at " + start_time)    
            
#Function that gets the date specified by the user. 
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    elif text.count("tomorrow") > 0:
        return datetime.date.today() + datetime.timedelta(days=1)
   
    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    
    if month < today.month and month != -1:
        year = year + 1
    
    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif +=7
        if text.count("next") >= 1:
            dif += 7           
        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)    
    
#Function that uses the Twilio API in order to send a message. 
#Users can only send messages to contacts that have a verified Twilio phone number. 
def send_message(friend_number, message):
    # Initialize the Twilio client
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    try:
        # Send the message
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=friend_number
        )
        print_and_speak("Message sent successfully!")
    except Exception as e:
        print("Failed to send message:", str(e))    

#Function that translates a phrase from one language to another.
#Takes user audio input, calls the listen() fucntion which converts the user's audio int a string.
#Calls the Translator() object in order to stranslate the phrase to a specified language.
#Saves the translated phrase as a .mp3 file, which is played back to the user and printed in the terminal. The .mp3 is then deleted
def translate_phrase(phrase_to_translate):
        tr = Translator()
        print_and_speak("What language would you like to translate this phrase to?")
        lang = listen()
        lang_code = get_language_code(lang)
        trans = tr.translate(phrase_to_translate, src='en', dest=lang)
        tts = gTTS(text=trans.text,lang=lang_code)
        tts.save("translated_phrase.mp3")
        print(trans.text)
        playsound("translated_phrase.mp3")
        os.remove("translated_phrase.mp3")

#Converts the language specified by the user to a 2 letter language code.
#The gTTS object can only take a 2 letter language code as input in order to translate a phrase to another language. 
def get_language_code(lang):
    for code, name in gtts.lang.tts_langs().items():
        if name.lower() == lang.lower():
            return code
    return None

#Function that authenticates usage for Google Calendar AOI
def google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 'n' events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


#Main function for the voice assistant. 
#The voice assistant will listen for it's name, Bizmo, which is the wake word.
#Once the wake word is detected, the user can then specify what task they want to accomplish.
#Tasks include searching the web, checking a schedule, sending a text message, and translating a phrase to another language.
#If the word "exit" is detected, the voice assistant will shut down and the program will end. 
def main():
    print("Starting to listen...")
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)  
            try: 
                #Voice assistant only works if the wake word is detected.
                command = r.recognize_google(audio)
                print(command)
                if command in wake_words:
                    print_and_speak("How can I help?")
                    command = listen()
                    #Search: Users specifies what they want to look up. A Google Chrome tab will open.
                    if "search" in command:
                        # Extract the search query from the command
                        query = command.replace("search", "").strip()
                        # Open a web browser and perform the search
                        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
                        engine.say(f"Searching for {query} on the web.")
                    #Schedule: Checks the users schedule with a specified date. 
                    elif "schedule" in command:
                        date = get_date(command)
                        print(date)
                        if date:
                            get_events(date, service)
                        else:
                            speak("Your instructions are unclear, please try again.")
                    #Text: Messages a person within the user;s contact list.       
                    elif "text" in command:
                        #Extract the friend's name from the command
                        friend_name = command.replace("text", "").strip()                  
                        if friend_name in CONTACTS:
                            print_and_speak("What message would you like to send?")
                            message=listen()                        
                            send_message(CONTACTS[friend_name], message)
                        else:
                            print_and_speak("This person is not in your contact list")
                    #Translate: Translated a phrase from one language to another.
                    elif "translate" in command:
                        phrase_to_translate = command.replace("translate", "").strip()
                        print(phrase_to_translate) 
                        translate_phrase(phrase_to_translate)
                    #Exit: End the program.   
                    elif "exit" in command:
                        print_and_speak("Powering down. See you soon.")
                        break                
                    else:
                        engine.say("Sorry, I didn't understand that command.")
                    
                    engine.runAndWait()
                    
                else:
                    print("Wake word not detected.")

            except Exception as e:
                print("Exception: Waiting for response" + str(e))
        

#Saves google credentials as service, which is used in calendar function calls.
service = google()

#Runs the voice assistant.
if __name__ == "__main__":
    main()





