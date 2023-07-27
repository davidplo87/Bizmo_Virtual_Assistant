# Bizmo_Virtual_Assistant
A Python script intended for a single user that can search the web, translate phrases to another language, text a friend, and check your schedule.

## How it works
This project uses the Google Calendar API, Twilio API, and speech recognition libraries. Bizmo, the voice assistant, takes audio input from the user and detects specified words in order to run commands. Bizmo will only listen for commands once it's name (the wake word) is detected. 

## Functionalities and wake words 
"Bizmo": This is the wake word. (Ex: when the wake word is detected, Bizmo will reply with "How can I help?" From there, Bizmo will start listening for a command.)
"Search": Allows the user to search the web. (Ex. "search beaches near me". This will open up a Google tab and search for "beaches near me".)
"Schedule": Reads the user's schedule for a specified day. (Ex: "what is my schedule for tomorrow?" This will check the user's schedule for the following day.)
"Text": Sends a text message to someone in the user's contact list. (Ex: "Text David". If there is someone named David in the user's contact list, Bizmo will ask "What message would you like to send?". From there, the user can say a phrase that will be sent as a text message to the specified contact.)
"Translate": Translates a phrase from one language to another. (Ex: "translate I want to go to the beach this weekend". Bizmo will then ask "What language would you like to translate this phrase to?". The user can tell Bizmo the target language. The phrase will be translated and played back to the user.)
"Exit": Ends the program.

## Setting up
You will need to enable the Google Calendar API and authorize your google credentails. For more information on how to get this set up, please visit this link (https://developers.google.com/calendar/api/quickstart/python?authuser=3). After following these steps, post the credentials.json file into the working directory. Once you run the program, a tab should open where you're able to sign into your google account. When you choose your Google account to sign in, an error will pop up saying "This app isn't verified". From there, click the "Advanced", click "Go to Quickstart", and click "allow" on the "Grant Quickstart permission" tab. Once this is completed, you will be able to close the window and run the program.



