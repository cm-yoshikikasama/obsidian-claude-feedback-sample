import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_today_events():
    creds = None
    credentials_path = os.path.join(os.path.dirname(__file__), 'cal_client_secret.json')
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=today.isoformat() + 'Z',
        timeMax=tomorrow.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # 今日の日付を出力
    print(f"DATE: {today.strftime('%Y-%m-%d')}")
    
    if not events:
        print("今日の予定はありません")
        return
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if 'T' in start:
            # 時刻付きの場合、時刻のみ表示
            time_part = datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%H:%M')
            print(f"{time_part} - {event['summary']}")
        else:
            # 終日イベントの場合
            print(f"終日 - {event['summary']}")

if __name__ == '__main__':
    get_today_events()
