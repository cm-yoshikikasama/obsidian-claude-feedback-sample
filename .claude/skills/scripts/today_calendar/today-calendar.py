import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------- 定数 ----------
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
JST = timezone(timedelta(hours=9))
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_PATH = SCRIPT_DIR / "cal_client_secret.json"
TOKEN_PATH = SCRIPT_DIR / "token.json"


def get_credentials() -> Credentials:
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())

    return creds


def get_events_for_date(target_date: str) -> None:
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    target_jst = datetime.strptime(target_date, "%Y-%m-%d").replace(
        tzinfo=JST, hour=0, minute=0, second=0, microsecond=0
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
    print(f"DATE: {target_jst.strftime('%Y-%m-%d')}")

    if not events:
        print(f"{target_jst.strftime('%Y-%m-%d')}の予定はありません")
        return

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        if "T" in start:
            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            jst_time = dt.astimezone(JST).strftime("%H:%M")
            print(f"{jst_time} - {event['summary']}")
        else:
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
