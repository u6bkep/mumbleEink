from __future__ import print_function
import datetime
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import codecs
import os
import iso8601

def update_cal():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    template = 'template.svg'

    google_calendar_id=os.getenv("GOOGLE_CALENDAR_ID","kettering.edu_8n2r3nu4gna8lomlr7fdqdnmr4@group.calendar.google.com")

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    events_result = None
    stale = True

    if(os.path.isfile(os.getcwd() + "/calendar.pickle")):
        print("Found cached calendar response")
        with open('calendar.pickle','rb') as cal:
            events_result = pickle.load(cal)
        stale=time.time() - os.path.getmtime(os.getcwd() + "/calendar.pickle") > (1*60*60)

    if stale:
        print("Pickle is stale, calling the Calendar API")
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=google_calendar_id, timeMin=now,
                                            maxResults=6, singleEvents=True,
                                            orderBy='startTime').execute()
        with open('calendar.pickle', 'wb') as cal:
            pickle.dump(events_result, cal)

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    output = codecs.open(template , 'r', encoding='utf-8').read()
    output = output.replace('CAL_DAY', iso8601.parse_date(events[0]['start']['dateTime']).strftime("%d"))
    #import pdb; pdb.set_trace()
    for i, event in enumerate(events):
        dateTimeStart = iso8601.parse_date(event['start']['dateTime'])
        #start = event['start'].get('dateTime', event['start'].get('date'))
        #import pdb; pdb.set_trace()
        #start = start[:10]
        #day = time.strftime("%a %b %d",time.strptime(start,"%Y-%m-%d"))
        desc = event['summary']
        #print(day, desc)
        print(desc)
        output = output.replace('CAL_DATE_{}'.format(i+1),dateTimeStart.strftime("%a %b %d"))
        output = output.replace('CAL_TIME_{}'.format(i+1),dateTimeStart.strftime("%-I:%M%p"))
        output = output.replace('CAL_DESC_{}'.format(i+1),desc)
        codecs.open('screen-output-cal.svg', 'w', encoding='utf-8').write(output)
    return output
    #codecs.open('screen-output-cal.svg', 'w', encoding='utf-8').write(output)
