import openai
import json
import logging
import datetime
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in chat_with_gpt: {str(e)}")
        return None

def parse_date(date_str):
    today = datetime.date.today()
    if '明日' in date_str:
        return today + datetime.timedelta(days=1)
    elif '明後日' in date_str:
        return today + datetime.timedelta(days=2)
    elif '今日' in date_str:
        return today
    else:
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return today

def parse_schedule_info(user_input):
    today_at_japan = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

    prompt = f"""
    日本語で書かれた以下の予定情報から、スケジュールの詳細を抽出してください：
    "{user_input}"
    
    以下の形式でJSONオブジェクトを返してください：
    {{
        "event_title": "イベントのタイトル",
        "date": "イベントの日付（「YYYY-MM-DD」形式）",
        "start_time": "開始時間（HH:MM形式、24時間表記）。指定がない場合はnull",
        "end_time": "終了時間（HH:MM形式、24時間表記）。指定がない場合はnull",
        "is_all_day": "終日イベントかどうか（true/false）"
    }}
    
    時間が指定されている場合は、必ずstart_timeとend_timeを設定し、is_all_dayをfalseにしてください。
    時間が指定されていない場合のみ、is_all_dayをtrueにしてください。
    日付が指定されていない場合は、今日の日付#{today_at_japan.strftime('%Y-%m-%d')}を設定してください。
    明日や明後日などの相対的な日付は、絶対的な日付に変換してください。
    JSONオブジェクトのみを返し、それ以外は何も付け加えないでください。
    """
    
    response = chat_with_gpt(prompt)
    if response:
        try:
            data = json.loads(response)
            if 'date' not in data or not data['date']:
                data['date'] = '今日'
            
            data['date'] = parse_date(data['date']).isoformat()
            
            if ('start_time' in data and data['start_time']) or ('end_time' in data and data['end_time']):
                data['is_all_day'] = False
            else:
                data['is_all_day'] = True

            return data
        except json.JSONDecodeError:
            logging.error(f"Failed to parse JSON from ChatGPT response: {response}")
    return None
