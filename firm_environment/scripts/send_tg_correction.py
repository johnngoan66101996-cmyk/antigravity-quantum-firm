import json
import urllib.request

def send_tg_correction():
    token = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
    chat_id = "8558082021"
    
    text = (
        "⚠️ <b>ВЕРИФИКАЦИЯ СТАТУСА RUTUBE:</b>\n\n"
        "Видео <code>antigravity_v25_promo.mp4</code> находится в локальном буфере и ожидает фактической отправки файла в Студию.\n"
        "Статус в Content Calendar возвращён в <b>🟡 BUFFERED</b>.\n\n"
        "Нажмите <b>[ + ]</b> в верхней панели Rutube для передачи файла с Рабочего стола."
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("[+] Sent correction to Telegram:", resp.status)
    except Exception as e:
        print("[-] Error sending to Telegram:", e)

if __name__ == "__main__":
    send_tg_correction()
