import logging
import os
import sys
from pathlib import Path

import ffmpeg
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.oauth2 import service_account

load_dotenv()

# ---------- 定数 ----------
PROJECT_ID = os.getenv("PROJECT_ID")
MODEL_NAME = "gemini-3-pro-preview"
LOCATION = "global"
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

MIME_TYPES = {
    ".mp3": "audio/mp3",
    ".mp4": "video/mp4",
    ".m4a": "audio/m4a",
}

PROMPT = """\
以下の音声を書き起こしてください。
1. 発言者が変わるたびに改行してください。
2. 可能であれば句読点を補ってください。
"""


# ---------- ロギング ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# ---------- クライアント（遅延初期化） ----------
_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if credentials_path and Path(credentials_path).exists():
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=SCOPES,
            )
            _client = genai.Client(
                vertexai=True,
                project=PROJECT_ID,
                location=LOCATION,
                credentials=credentials,
            )
        else:
            _client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    return _client


# ---------- 関数 ----------
def convert_mp4_to_mp3(mp4_path: Path, mp3_path: Path) -> None:
    logger.info("MP4→MP3変換: %s", mp4_path.name)
    ffmpeg.input(str(mp4_path)).output(str(mp3_path)).global_args(
        "-loglevel", "quiet"
    ).run(overwrite_output=True)


def get_mime_type(path: Path) -> str:
    mime_type = MIME_TYPES.get(path.suffix.lower())
    if not mime_type:
        raise ValueError(f"サポートされていないファイル形式: {path.suffix}")
    return mime_type


def transcribe(audio_path: Path) -> str:
    logger.info("文字起こし開始: %s", audio_path.name)
    audio_part = types.Part.from_bytes(
        data=audio_path.read_bytes(),
        mime_type=get_mime_type(audio_path),
    )
    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=[audio_part, PROMPT],
    )
    logger.info("文字起こし完了")
    return response.text


def get_input_files() -> list[Path]:
    return [
        f
        for f in INPUT_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.suffix.lower() in MIME_TYPES
    ]


def process_file(file_path: Path) -> Path:
    logger.info("処理開始: %s", file_path.name)
    temp_mp3 = None

    if file_path.suffix.lower() == ".mp4":
        temp_mp3 = file_path.with_name(f"{file_path.stem}_converted.mp3")
        convert_mp4_to_mp3(file_path, temp_mp3)
        audio_path = temp_mp3
    else:
        audio_path = file_path

    transcript = transcribe(audio_path)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{file_path.stem}_transcript.txt"
    output_path.write_text(transcript, encoding="utf-8")
    logger.info("保存完了: %s", output_path.name)

    if temp_mp3 and temp_mp3.exists():
        temp_mp3.unlink()
        logger.info("一時ファイル削除: %s", temp_mp3.name)

    # 入力ファイル削除
    file_path.unlink()
    logger.info("入力ファイル削除: %s", file_path.name)

    return output_path


def cleanup_output() -> None:
    """出力ディレクトリ内のファイルを全削除"""
    if not OUTPUT_DIR.exists():
        return
    for f in OUTPUT_DIR.iterdir():
        if f.is_file() and not f.name.startswith("."):
            f.unlink()
            logger.info("出力ファイル削除: %s", f.name)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_output()
        logger.info("クリーンアップ完了")
        return

    input_files = get_input_files()
    if not input_files:
        logger.warning("対応ファイルがありません")
        raise SystemExit(1)

    logger.info("検出: %s", [f.name for f in input_files])
    for file_path in input_files:
        process_file(file_path)
    logger.info("完了")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("エラー: %s", e)
        raise
