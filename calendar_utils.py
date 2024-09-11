from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import logging
from config import GOOGLE_CALENDAR_SCOPES, GOOGLE_CALENDAR_SERVICE_ACCOUNT_FILE, GOOGLE_CALENDAR_ID

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CALENDAR_SERVICE_ACCOUNT_FILE, scopes=GOOGLE_CALENDAR_SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def add_event_to_calendar(schedule_info):
    try:
        event_date = schedule_info['date']

        if schedule_info['is_all_day']:
            event_body = {
                'summary': schedule_info['event_title'],
                'start': {'date': event_date},
                'end': {'date': event_date},
            }
        else:
            start_time = schedule_info.get('start_time', '00:00')
            end_time = schedule_info.get('end_time')
            
            if not end_time:
                start_dt = datetime.datetime.fromisoformat(f"{event_date}T{start_time}:00")
                end_dt = start_dt + datetime.timedelta(hours=1)
                end_time = end_dt.strftime("%H:%M")

            start_datetime = f"{event_date}T{start_time}:00"
            end_datetime = f"{event_date}T{end_time}:00"

            event_body = {
                'summary': schedule_info['event_title'],
                'start': {'dateTime': start_datetime, 'timeZone': 'Asia/Tokyo'},
                'end': {'dateTime': end_datetime, 'timeZone': 'Asia/Tokyo'},
            }
    
        event = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event_body).execute()
        logging.info(f"Event added to calendar: {event.get('htmlLink')}")
        return True
    except HttpError as error:
        logging.error(f"An error occurred while adding event to calendar: {error}")
        return False
