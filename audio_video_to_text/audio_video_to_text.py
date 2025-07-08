import os
import logging
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv
import ffmpeg


# .envファイルの読み込み
load_dotenv()

# ---------- 環境変数 ----------
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
FILE_NAME = os.getenv("FILE_NAME")  # 例: "meeting_audio.mp4" または "meeting_audio.mp3"
OUTPUT_DIR = "output"  # 出力先
MODEL_NAME = "gemini-2.5-pro-preview-03-25"
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

# ---------- ロギング ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Vertex AI の初期化
vertexai.init(project=PROJECT_ID, location=REGION)


def convert_mp4_to_mp3(mp4_path: str, mp3_path: str) -> None:
    """MP4 ファイルをMP3に変換"""
    logger.info("MP4からMP3への変換開始: %s -> %s", mp4_path, mp3_path)
    try:
        (
            ffmpeg.input(mp4_path)
            .output(mp3_path)
            .global_args("-loglevel", "quiet")
            .run(overwrite_output=True)
        )
        logger.info("MP4からMP3への変換完了")
    except Exception as e:
        logger.error("MP4変換中にエラーが発生しました: %s", e)
        raise


def transcribe_audio(audio_path: str) -> str:
    """音声ファイルをテキストに書き起こす"""
    logger.info("文字起こし開始: %s", audio_path)

    model = GenerativeModel(MODEL_NAME)

    # ファイル拡張子に基づいてMIMEタイプを決定
    if audio_path.lower().endswith('.mp4'):
        mime_type = "video/mp4"
    elif audio_path.lower().endswith('.mp3'):
        mime_type = "audio/mp3"
    else:
        raise ValueError(f"サポートされていないファイル形式: {audio_path}")

    with open(audio_path, "rb") as f:
        audio_part = Part.from_data(f.read(), mime_type=mime_type)

    prompt = (
        "以下の音声を書き起こしてください。\n"
        "1. 発言者が変わるたびに改行してください。\n"
        "2. 可能であれば句読点を補ってください。\n"
    )

    response = model.generate_content([audio_part, prompt])
    logger.info("文字起こし完了")
    return response.text


if __name__ == "__main__":
    try:
        # ファイル名と拡張子を分離
        input_file_path = os.path.join("input", FILE_NAME)
        file_name_without_ext, file_extension = os.path.splitext(FILE_NAME)
        
        # 入力ファイルの存在確認
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"入力ファイルが見つかりません: {input_file_path}")
        
        audio_file = None
        temp_mp3_file = None
        
        if file_extension.lower() == ".mp4":
            # MP4ファイルの場合、MP3に変換
            temp_mp3_file = os.path.join("input", f"{file_name_without_ext}_converted.mp3")
            convert_mp4_to_mp3(input_file_path, temp_mp3_file)
            audio_file = temp_mp3_file
        elif file_extension.lower() == ".mp3":
            # MP3ファイルの場合、そのまま使用
            audio_file = input_file_path
        else:
            raise ValueError(f"サポートされていないファイル形式: {file_extension}")

        # 文字起こし実行
        transcript = transcribe_audio(audio_file)

        # 出力保存（拡張子なしのファイル名を使用）
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, f"{file_name_without_ext}_transcript.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info("書き起こしテキストを保存しました: %s", out_path)
        
        # 一時ファイルの削除
        if temp_mp3_file and os.path.exists(temp_mp3_file):
            os.remove(temp_mp3_file)
            logger.info("一時ファイルを削除しました: %s", temp_mp3_file)

    except Exception as e:
        logger.exception("処理中にエラーが発生しました: %s", e)
        raise
