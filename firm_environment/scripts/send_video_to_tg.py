import json
import urllib.request
from pathlib import Path

TOKEN = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
CHAT_ID = "8558082021"

def send_telegram_video():
    video_path = Path(r"C:\Users\sugat\OneDrive\Desktop\antigravity_v25_promo.mp4")
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    with open(video_path, "rb") as f:
        video_bytes = f.read()
        
    body = bytearray()
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{CHAT_ID}\r\n".encode())
    caption = "🎥 <b>ГОТОВЫЙ ПРОМО-РОЛИК (1080p CINEMATIC):</b>\nANTIGRAVITY v2.5 — Промышленный торговый комплекс и квантовые агенты L2.\n\n5 сцен на базе 8K нейросетевых рендеров. Нажмите 'Одобряю' для запуска браузерной заливки на Rutube!"
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parse_mode\"\r\n\r\nHTML\r\n".encode())
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"video\"; filename=\"antigravity_v25_promo.mp4\"\r\nContent-Type: video/mp4\r\n\r\n".encode())
    body.extend(video_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode())
    
    print(f"[*] Sending video ({len(video_bytes)} bytes) to Telegram...")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            res = json.loads(resp.read().decode())
            print(f"[+] Video delivered to Telegram successfully: {res.get('ok')}")
            return True
    except Exception as e:
        print(f"[-] Error sending video to Telegram: {e}")
        return False

if __name__ == "__main__":
    send_telegram_video()
