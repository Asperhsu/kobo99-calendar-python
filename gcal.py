from datetime import timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_PROD_ID = 'rcmvnfej75s7c9sjdbic1f55v8@group.calendar.google.com'
CALENDAR_TEST_ID = 'rqcl9m6ucfca9vp67afvi3bdhk@group.calendar.google.com'
CALENDAR_ID = CALENDAR_PROD_ID

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=credentials)

def list_events(mindate, maxdate):
    service = get_calendar_service()

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=mindate.isoformat()  + 'T00:00:00+08:00',
        timeMax=maxdate.isoformat()  + 'T23:59:59+08:00',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return events

def create_event(book):
    service = get_calendar_service()

    body = {
        "summary": book['title'],
        "description": book['description'],
        "start": {"date": book['date'].isoformat(), "timeZone": 'Asia/Taipei'},
        "end": {"date": (book['date'] + timedelta(days=1)).isoformat(), "timeZone": 'Asia/Taipei'},
        "extendedProperties": {
            "shared": {
                "id": book['id']
            }
        }
    }
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
    print("Event created:",  book['title'])

def event_by_book_id(events, id):
    for event in events:
        if event.get('extendedProperties', {}).get('shared', {}).get('id') == id: return event;
    return None;