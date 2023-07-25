#config.py
#All global variable that will be used in main.py

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january","february","march","april","may","june","july","august","septemeber","october","november","december"]
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAY_EXTENTIONS = ["rd","th","st","nd"]
#CALENDAR_STRS=["what do i have", "do i have plans","am i busy", "what are my plans", "what's my schedule"]
CONTACTS = {'Contact1': '+17777777777',
            'Contact2': '+18888888888',
            'Contact3': '+19999999999',
            'Contact4': '+12222222222',
            'Contact5': '+13333333333',
}

#USER MUST ENTER THEIR OWN PRIVATE TWILIO SID AND AUTH TOKEN HERE
#DO NOT SHARE THIS DATA WITH ANYONE AND KEEP THESE CODES IN A SAFE PLACE. 
TWILIO_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER = ''