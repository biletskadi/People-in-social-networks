from __future__ import print_function

from typing import List, Any, Tuple

import json
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class Calendar:
    """
    This class works with Google calendar,
    it creates, deletes and changes events, 
    shows events.
    """
    def __init__(self):
        self.service = None

    def startCommand(self, bot, update):
        """
        This function starts a bot and authorises user into google account
        """
        bot.send_message(chat_id=update.message.chat_id, text="Привіт! \n"
                                                              "Я допоможу Вам організувати свій календар та прокласти маршрут до місця події!"
                                                              "\nЩоб переглянути усі функції натисніть /help")
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        bot.send_message(chat_id=update.message.chat_id,
                         text="https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=558268665760-efbmhgve4ovnendbv5um6sr5o1shqd4a.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A62799%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&state=wLSAOuK4H1CvlrgIifQgH9zte1nvcF&access_type=offline")
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials = creds)

    def AddMessage(self, bot, update):
        """
        This function adds an event to your calendar
        """
        bot.send_message(chat_id=update.message.chat_id, text="Яка назва події")
        name = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Яка дата події(у форматі рр/мм/дд, наприклад 2020-06-30)")
        date = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Який час початку події(у фораті год:хв, наприклад 10:15)")
        start = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Який час закінчення події(у фораті год:хв, наприклад 10:15)")
        end = update.message.text        
        event = {
            'summary': str(name),
            'start': {
                'dateTime': str(date) + 'T' + str(start) + ':00+03:00',
            },
            'end': {
                'dateTime': str(date) + 'T' + str(end) + ':00+03:00',
            },
            'attendees': [
                {'email': 'biletska@ucu.edu.ua'},
                {'email': 'bas@ucu.edu.ua'},
            ],
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        bot.send_message(chat_id=update.message.chat_id, text='Подію створено {}'.format(event.get('htmlLink')))

    def DeleteMessage(self, bot, update):
        """
        this function deletes an event from clendar
        """
        bot.send_message(chat_id=update.message.chat_id, text="Яка назва події")
        name = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Яка дата події(у форматі рр/мм/дд, наприклад 2020-06-30)")
        date = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Який час початку події(у фораті год:хв, наприклад 10:15)")
        start = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Який час закінчення події(у фораті год:хв, наприклад 10:15)")
        end = update.message.text  

    def ChangeMessage(self, bot, update):
        """
        this function makes changes to the event
        """
        bot.send_message(chat_id=update.message.chat_id, text="Яка назва події")
        name = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Яка дата події(у форматі рр/мм/дд, наприклад 2020-06-30)")
        date = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Який час початку події(у фораті год:хв, наприклад 10:15)")
        start = update.message.text
        bot.send_message(chat_id=update.message.chat_id, text="Який час закінчення події(у фораті год:хв, наприклад 10:15)")
        end = update.message.text  
    def CheckDailyMessage(self, bot, update):
        """
        this function shows events per one day
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z' 
        bot.send_message(chat_id=update.message.chat_id, text='Події на сьогодні')
        events_result = self.service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                                   orderBy='startTime', datetime = update.message.text).execute()
        events = events_result.get('items', [])
        events_lst = []
        if not events:
            bot.send_message(chat_id=update.message.chat_id, text='Немає подій на сьогодні.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            # events_lst.append(str(start).strip('T') + " - " + str(event['summary']) + '\n\n')
            events_lst.append(
                str(start).split('T')[0] + "  -  " + str(event['summary']) + '  -  ' +
                str(start).split('T')[1].split(':')[0] + ':' +
                str(start).split('T')[1].split(':')[1] + '\n\n')
        eventss = ''.join(events_lst)
        bot.send_message(chat_id=update.message.chat_id, text=eventss)

    def CheckNextEventsMessage(self, bot, update):
        """
        this function shows the next n events in your calendar
        """
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=int(update.message.text), singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        events_lst = []
        if not events:
            bot.send_message(chat_id=update.message.chat_id, text='Немає подій найближчим часом')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            # events_lst.append(str(start).strip('T') + " - " + str(event['summary']) + '\n\n')
            events_lst.append(
                str(start).split('T')[0] + "  -  " + str(event['summary']) + '  -  ' +
                str(start).split('T')[1].split(':')[0] + ':' +
                str(start).split('T')[1].split(':')[1] + '\n\n')
        eventss = ''.join(events_lst)
        bot.send_message(chat_id=update.message.chat_id, text=eventss)