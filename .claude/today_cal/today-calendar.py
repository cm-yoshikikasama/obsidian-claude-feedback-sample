import os
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_today_events():
    creds = None
    credentials_path = os.path.join(os.path.dirname(__file__), "cal_client_secret.json")
    token_path = os.path.join(os.path.dirname(__file__), "token.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    # JST (UTC+9) のタイムゾーンを定義
    jst = timezone(timedelta(hours=9))

    # JST の今日の日付を取得
    today_jst = datetime.now(jst).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_jst = today_jst + timedelta(days=1)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=today_jst.isoformat(),
            timeMax=tomorrow_jst.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    # 今日の日付を出力
    print(f"DATE: {today_jst.strftime('%Y-%m-%d')}")

    if not events:
        print("今日の予定はありません")
        return

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        if "T" in start:
            # 時刻付きの場合、JSTに変換して時刻のみ表示
            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            jst_time = dt.astimezone(jst).strftime("%H:%M")
            print(f"{jst_time} - {event['summary']}")
        else:
            # 終日イベントの場合
            print(f"終日 - {event['summary']}")


if __name__ == "__main__":
    get_today_events()
