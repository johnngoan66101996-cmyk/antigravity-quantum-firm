import json
import urllib.request
from pathlib import Path

TOKEN = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
CHAT_ID = "8558082021"

def send_telegram_photo(photo_path: Path, caption: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    with open(photo_path, "rb") as f:
        photo_bytes = f.read()
        
    body = bytearray()
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{CHAT_ID}\r\n".encode())
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parse_mode\"\r\n\r\nHTML\r\n".encode())
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{photo_path.name}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode())
    body.extend(photo_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode())
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode())
            print(f"[+] Photo {photo_path.name} sent: {res.get('ok')}")
            return True
    except Exception as e:
        print(f"[-] Error sending photo {photo_path.name}: {e}")
        return False

def main():
    brain_dir = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
    scene4_path = brain_dir / "scene_4_cybernetic_vault_shield_1793774307929.jpg"
    if scene4_path.exists():
        send_telegram_photo(
            scene4_path, 
            "<b>Сцена 4: Бескомпромиссный риск-менеджмент</b>\n<i>Кибернетический силовой щит, аппаратный стоп-лосс 25 bps и контур самоисцеления Actor-Critic.</i>"
        )

if __name__ == "__main__":
    main()
