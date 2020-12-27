from __future__ import print_function
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main(pathToCred, summary, description, location, startTime, endTime, attendees):

    creds = None

    def authCal(path):

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    pathToCred, SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    def eventJson(summary,location,description,startTime,endTime,attendees):

        EVENT = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': startTime,
            'timeZone': 'Asia/Calcutta',
        },
        'end': {
            'dateTime': endTime,
            'timeZone': 'Asia/Calcutta',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': attendees[0]},
            {'email': attendees[1]}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
            }
        return EVENT

    service = authCal(pathToCred)

    EVENT=eventJson(summary, description, location, startTime, endTime, attendees)

    e = service.events().insert(calendarId='primary', sendNotifications=True, body=EVENT).execute()


if __name__ == '__main__':
    pathToCred = sys.argv[1]
    summary = sys.argv[2]
    description = sys.argv[3]
    location = sys.argv[4]
    startTime = sys.argv[5]
    endTime = sys.argv[6]
    attendees = sys.argv[7]
    print(sys.argv)
    main(pathToCred, summary, description,location, startTime, endTime, attendees.split(","))
