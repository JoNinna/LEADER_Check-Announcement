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
keywords = ["Anunt ANIMARE-Iulie 2025", "Anunt ANIMARE-Septembrie 2025", "Anunt ANIMARE-Octombrie 2025"]

# Configurație Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN").strip()
CHAT_ID = os.getenv("CHAT_ID").strip()

def send_telegram(message: str) -> bool:
    # Trimite mesaj Telegram pentru raspuns API
    if not CHAT_ID or not BOT_TOKEN:
        print(f"[Eroare] Credentiale necorespunzatoare!")
        return False
    
    urltelegram=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        responsetelegram=requests.post(urltelegram, params={"chat_id": CHAT_ID, "text": message}, timeout=15)
        ok = responsetelegram.status_code == 200 and responsetelegram.json().get("ok") is True
        print("Mesajul a fost trimis pe Telegram!", responsetelegram.json())
        return ok
    except Exception as e:
        print(f"Eroare la trimiterea pe Telegram: {e}")
        return False

def check_page(url: str, keywords: list[str]) -> bool:
    try:
        response=requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 Leader Check/1.0"})
        print(f"[HTTP] GET {url} {response.status_code}, {len(response.text)} bytes")
        response.raise_for_status()
        content=response.text.lower()

        for key in keywords:
            if key.lower() in content:
                print("A aparut o postare de interes pe pagina!")
                send_telegram(f"ALERTA! A aparut rublica {key}")
                return True
        return False
    except Exception as e:
        print(f"Eroare la acesarea paginii")
        send_telegram(f"Eroare la acesarea paginii: {e} ")
        return False

if __name__ == "__main__":
    # Pentru testare:
    # found=check_page(url, keywords)
    # print(f"Rezultat {found}")
    while True:
        print(f"Verificare site la {datetime.now()}")
        found=check_page(url, keywords)
        if not found:
            print("Rublica nu a fost publicata!")
        # Site-ul este verificat o data pe zi
        time.sleep(86400)