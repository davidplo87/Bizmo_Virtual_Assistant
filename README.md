# Bizmo_Virtual_Assistant
A Python script that can search the web, translate phrases to another language, text a friend, and check your schedule.

## How it works
This projects uses the Google Calendar API, Twilio API, and speech recognition libraries. Bizmo, the voice assistant, takes audio input from the user and detects specified words in order to run commands. Bizmo will only listen for commands once it's name (the wake word) is detected. 

## Functionalities and wake words 
"Bizmo": this is the wake word. (Ex: when the wake word is detected, Bizmo will reply with "How can I help?". From there, Bizmo will start listening for a command.)
"Search": allows the user to search the web. (Ex. "search beaches near me". This will open up a Google tab and search for "beaches near me".) 
"Schedule": reads the users schedule for a specified day. (Ex: "what is my schedule for tomorrow?" This will check the users schedule for the following day.)
"Text": sends a text message to someone in the user's contact list. (Ex: "Text David". If there is someone named David in the user's contact list, Bizmo will ask "What message would you like to send?". From there, the user          can say a phrase that will be sent as a text message to the specified contact.) 
"Translate": translates a phrase from one language to another. (Ex: "translate I want to go to beach this weekend". Bizmo will then ask "What language would you like to translate this phrase to?". The user can tell Bizmo            the target language. The phrase will be translated and played back to the user. 
"Exit": ends the program.





