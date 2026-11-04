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
    scene3_path = brain_dir / "scene_3_orderbook_spread_capture_1793774204899.jpg"
    if scene3_path.exists():
        send_telegram_photo(
            scene3_path, 
            "<b>Сцена 3: Захват спреда и геометрия зон Z1, Z2, Z3</b>\n<i>Математика Авелланеды-Стойкова, глубина стакана L2 и лазерные уровни входа.</i>"
        )

if __name__ == "__main__":
    main()
