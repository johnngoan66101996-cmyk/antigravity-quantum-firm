import json
import urllib.request
from pathlib import Path

def send_tg_notification():
    token = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
    chat_id = "8558082021"
    
    text = (
        "🚀 <b>НОВОЕ ВИДЕО ОПУБЛИКОВАНО НА RUTUBE!</b>\n\n"
        "📺 <b>Канал:</b> Квантовый ИИ: Claude Code, GPT & Нейросети\n"
        "🎬 <b>Название:</b> ANTIGRAVITY v2.5: Промышленный торговый комплекс и квантовые агенты L2\n"
        "📦 <b>Статус в Content Calendar:</b> 🟢 PUBLISHED\n"
        "🐙 <b>GitHub:</b> <a href='https://github.com/johnngoan66101996-cmyk/antigravity-quantum-firm'>antigravity-quantum-firm</a>\n"
        "⚡ <b>Торговый модуль:</b> Установлено 11 скиллов пакета trader-skill\n\n"
        "<i>Автономный цикл переведён в режим трекинга конверсий и товарного сканирования.</i>"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print("[+] Telegram notification delivered successfully:", data.get("ok"))
    except Exception as e:
        print("[-] Error sending Telegram notification:", e)

if __name__ == "__main__":
    send_tg_notification()
