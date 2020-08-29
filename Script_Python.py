from __future__ import print_function

import os
import httplib2
import time
import requests
import pickle

import pandas as pd

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'GovernanceProject'


def get_credentials():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def read_excel_happy_birthdays(file_name, sheet_name):
    """Reads an excel file which has the name file_name and the sheet sheet_name and
       extracts co-workers names and birthday dates.
    :param file_name: str. Excel file name
    :param sheet_name: str. Sheet in the excel file to read.
    :return: co_workers, dict. Dict with the co-workers names and birthday dates
    """
    co_workers = {}
    # Reads the excel file with pandas.
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    # Fills the null fields.
    df = df.fillna('')
    # Expects columns NAME, MONTH, DAY.
    for i in range(len(df["NAME"])):
        if df["NAME"][i] not in co_workers:
            # Formatting DAY and MONTH to values between  01 - 09.
            day = str(df["DAY"][i]).strip()
            month = str(df["MONTH"][i]).strip()
            if len(day) <= 1:
                day = '0' + day
            if len(month) <= 1:
                month = '0' + month
            co_workers[df["NAME"][i]] = [day, month]
    return co_workers


def create_events(service, events):
    """ Creates happy birthday events for co-workers.
    :param service: Google Calendar API
    :param events: dict. The co-workers names and birthday dat
    """
    for j in events:
        now = datetime.now()
        birthday = datetime(now.year, int(events[j][1]), int(events[j][0]))
        year = now.year
        # Compare if the birthday already happen. If birthday already happen postpone for the next year.
        if now > birthday:
            year = year + 1
        # Meeting day
        start = '{0}-{1}-{2}T12:15:00-05:00'.format(year, events[j][1], events[j][0])
        end = '{0}-{1}-{2}T12:30:00-05:00'.format(year, events[j][1], events[j][0])
        # Event body.  Turns to False the property sendNotifications for not send SPAM notifications.
        event = {
            'summary': 'Cumpleaños ' + j,
            'description': 'Hola,' + j + ' .' +
                           'El objetivo de la reunión es poderte cantar todos juntos tú cumpleaños, expresarte' +
                           ' nuestros mejores deseos y recordarte que para nosotros es muy grato contar contigo en el equipo.' +
                           ' Muchas Felicidades!',
            'start': {'dateTime': start, 'timeZone': 'America/Bogota'},
            'end': {'dateTime': end, 'timeZone': 'America/Bogota'},
            'recurrence': ['RRULE:FREQ=YEARLY;COUNT=3'],
            'attendees': [{'email': 'ejemplo.co.group@empresa.com'},
                          {'email': 'jefe@empresa.com'}],
            'sendNotifications': True,
            'conferenceData': {'createRequest': {'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                                                 'requestId': 'kdb-atdx-exx'}}
        }
        print(event)
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        print('Event created: %s' % (event.get('htmlLink')))


def test_event(service):
    """ TEST METHOD.
        YOU CAN DELETE, IF YOU WANT.
    :param service:
    :return:
    """
    now = datetime.now()
    start = '{0}-{1}-{2}T12:15:00-05:00'.format(now.year, now.month, now.day)
    end = '{0}-{1}-{2}T12:30:00-05:00'.format(now.year, now.month, now.day)
    event = {
        'summary': 'PRUEBA',
        'description': 'PRUEBA',
        'start': {'dateTime': start, 'timeZone': 'America/Bogota'},
        'end': {'dateTime': end, 'timeZone': 'America/Bogota'},
        'attendees': [{'email': 'pepito.perez@empresa.com'}],
        'reminders': {'useDefault': True},
        'sendNotifications': True,
        'conferenceData': {'createRequest': {'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                                             'requestId': 'kdb-atdx-exx'}}
    }
    print(event)
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def main():
    # Authentication with Google, Don't forget to enable Google API.
    print("AUTENTICANDO......")
    credentials = get_credentials()
    service = discovery.build('calendar', 'v3', credentials=credentials)
    print("AUTENTICACION CON EXITO.....")
    print("LECTURA EXCEL CUMPLES......")
    # Download the Excel file with co-workers birthdays.
    co_workers_db = read_excel_happy_birthdays("Equipo de trabajo.xlsx", "Cumple script eventos")
    print("FINAL LECTURA EXCEL CUMPLES......")
    print("CREANDO EVENTOS CUMPLES......")
    # Uncomment the method to use.
    #  create_events(service, co_workers_db)
    #  test_event(service)
    print("FINAL CREACION EVENTOS CUMPLES......")


if __name__ == '__main__':
    main()
