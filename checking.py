import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

# Incarca token-urile din env
load_dotenv()

# URL-ul paginii de monitorizat
url="https://gal-dsgh.ro/leader-2023-2027/category/evenimente-de-animare/"

# Termeni de cautat
keyworks = ["Anunt ANIMARE-Iulie 2025", "Anunt ANIMARE-Septembrie 2025", "Anunt ANIMARE-Octombrie 2025"]

# Configurație Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")   
CHAT_ID = os.getenv("CHAT_ID")         

def check_page(url: str, keywords: list[str]) -> bool:
    try:
        response=requests.get(url)
        response.raise_for_status()
        content=response.text.lower()

        for key in keyworks:
            if key.lower() in content:
                send_telegram(f"ALERTA! A aparut rublica {key}")
                return True
        return False
    except Exception as e:
        send_telegram(f"Eroare la acesarea paginii: {e} ")
        return False
    
def send_telegram(message):
    try:
        urltelegram=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        responsetelegram=requests.post(urltelegram, params={"chat_id": CHAT_ID, "text": message})
        print("Mesajul a fost trimis pe Telegram!", responsetelegram.json())
    except Exception as e:
        print(f"Eroare la trimiterea pe Telegram: {e}")

if __name__ == "__maine__":
    while True:
        print(f"Verificare site la {datetime.now()}")
        found=check_page()
        if not found:
            print("Rublica nu a fost publicata!")
        # Site-ul este verificat o data pe zi
        time.sleep(86400)