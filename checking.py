import os
import requests
from dotenv import load_dotenv

# Incarca token-urile din env
load_dotenv()

# Configurație Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")   
CHAT_ID = os.getenv("CHAT_ID")         
MESSAGE="Testul de la ora 5:35"

url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response=requests.post(url, params={"chat_id": CHAT_ID, "text": MESSAGE})

print(response.status_code)
print(response.json())