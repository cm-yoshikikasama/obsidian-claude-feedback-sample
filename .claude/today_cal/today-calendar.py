import os
import argparse
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_events_for_date(target_date):
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

    # 指定された日付をパース
    target_jst = datetime.strptime(target_date, "%Y-%m-%d").replace(
        tzinfo=jst, hour=0, minute=0, second=0, microsecond=0
    )

    next_day_jst = target_jst + timedelta(days=1)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=target_jst.isoformat(),
            timeMax=next_day_jst.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    # ターゲット日付を出力
    print(f"DATE: {target_jst.strftime('%Y-%m-%d')}")

    if not events:
        print(f"{target_jst.strftime('%Y-%m-%d')}の予定はありません")
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
    parser = argparse.ArgumentParser(
        description="Get Google Calendar events for a specific date"
    )
    parser.add_argument(
        "--date", type=str, required=True, help="Target date in YYYY-MM-DD format"
    )
    args = parser.parse_args()

    get_events_for_date(args.date)
