import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.readonly"]


#function to authorize a new user
def authorize():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds


#function to create and/or retrieve our calendar
def get_health_calendar(service):
  #first get a list of calendars
  page_token = None
  calendar_exists = False
  health_calendar = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      if (calendar_list_entry['summary'] == 'Health Calendar'):
        calendar_exists = True
        health_calendar = calendar_list_entry
        print(f"found calendar with id: {health_calendar['id']}")
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break
  if not calendar_exists:
    calendar = {
      'summary': 'Health Calendar',
      'timeZone': 'America/Los_Angeles'
    }
    health_calendar = service.calendars().insert(body=calendar).execute()
    print(f"created calendar with id: {health_calendar['id']}")
  return health_calendar

#function to create events
def create_event(service, health_calendar, event_info):
  event = service.events().insert(calendarId=health_calendar['id'], body=event_info).execute()
  print(f"Event created: {event.get('htmlLink')}")
  return event

def create_recommended_event(event_name, location, description, start_timedate, end_timedate):
  creds = authorize()

  try:
    service = build("calendar", "v3", credentials=creds)
    health_calendar = get_health_calendar(service)
    event = {
      'summary': event_name,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_timedate,
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': end_timedate,
        'timeZone': 'America/Los_Angeles',
      },
    }
    create_event(service, health_calendar, event)

  except HttpError as error:
    print(f"An error occurred: {error}")

#use this function to test
def main():
  creds = authorize()

  try:
    service = build("calendar", "v3", credentials=creds)
    health_calendar = get_health_calendar(service)
    event = {
      'summary': 'Test Event',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'This is a test event',
      'start': {
        'dateTime': '2024-06-24T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2024-06-24T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
    }
    my_event = create_event(service, health_calendar, event)

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()