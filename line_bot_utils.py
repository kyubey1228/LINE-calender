from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
from config import LINE_CHANNEL_ACCESS_TOKEN
from openai_utils import parse_schedule_info
from calendar_utils import add_event_to_calendar

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

def process_message(message, reply_token):
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(parse_schedule_info, message)
            schedule_info = future.result(timeout=25)

        logging.info(f"Parsed schedule info: {schedule_info}")
        
        if not schedule_info:
            return send_reply_message(reply_token, "申し訳ありません。スケジュール情報の解析に失敗しました。「明日15時から会議」のように、より具体的な情報を含めて入力してください。")

        success = add_event_to_calendar(schedule_info)
        if success:
            if schedule_info['is_all_day']:
                reply_message = f"スケジュール「{schedule_info['event_title']}」を{schedule_info['date']}の終日予定としてカレンダーに追加しました。"
            else:
                start_time = schedule_info['start_time'] or '不明'
                end_time = schedule_info['end_time'] or '不明'
                reply_message = f"スケジュール「{schedule_info['event_title']}」を{schedule_info['date']} {start_time}から{end_time}までの予定としてカレンダーに追加しました。"
        else:
            reply_message = "スケジュールの追加中にエラーが発生しました。"

    except TimeoutError:
        reply_message = "処理に時間がかかりすぎています。もう一度お試しください。"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {traceback.format_exc()}")
        reply_message = "予期せぬエラーが発生しました。"

    logging.info(f"Reply message: {reply_message}")
    send_reply_message(reply_token, reply_message)

def send_reply_message(reply_token, message):
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=message)]
                )
            )
    except Exception as e:
        logging.error(f"Failed to send reply message: {traceback.format_exc()}")
