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
    
    # chat_id
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{CHAT_ID}\r\n".encode())
    
    # caption
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    
    # parse_mode
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parse_mode\"\r\n\r\nHTML\r\n".encode())
    
    # photo
    filename = photo_path.name
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{filename}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode())
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
            print(f"[+] Photo {filename} sent successfully: {res.get('ok')}")
            return True
    except Exception as e:
        print(f"[-] Error sending photo {filename}: {e}")
        return False

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print("[+] Text message sent successfully")
            return True
    except Exception as e:
        print("[-] Error sending text:", e)
        return False

def main():
    brain_dir = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
    
    scene1_path = brain_dir / "cybernetic_financial_data_stream_1793771807999.jpg"
    scene2_path = brain_dir / "scene_2_dual_ai_core_1793774031102.jpg"
    
    send_telegram_message("🎬 <b>КОНТЕНТ-ПАКЕТ НА ОДОБРЕНИЕ ПЕРЕД ЗАЛИВКОЙ НА RUTUBE</b>\n\nНиже направляю сгенерированные 8K нейросетевые кадры и параметры публикации.")
    
    if scene1_path.exists():
        send_telegram_photo(scene1_path, "<b>Сцена 1: Вступление — Хаос рынка и микроструктура стакана L2</b>\n<i>Octane Render 8K, неоновые потоки данных и стакан котировок.</i>")
        
    if scene2_path.exists():
        send_telegram_photo(scene2_path, "<b>Сцена 2: Дуэт нейросетей Qwen-2.5 и DeepSeek-R1</b>\n<i>Нейронное око Qwen (слева) сканирует стакан, золотой мозг DeepSeek-R1 (справа) вычисляет математическое преимущество.</i>")
        
    meta_text = (
        "📋 <b>SEO-МЕТАДАННЫЕ ПУБЛИКАЦИИ:</b>\n\n"
        "📌 <b>Название:</b> ANTIGRAVITY v2.5: Промышленный торговый комплекс и квантовые агенты L2\n\n"
        "📝 <b>Описание:</b>\n"
        "Демонстрация работы автономного квантово-когнитивного ядра и торговых агентов Antigravity v2.5.\n"
        "- Высокочастотный арбитраж L2 (стакан котировок, Avellaneda-Stoikov)\n"
        "- Квантовая суперпозиция рыночных гипотез (Hadamard)\n"
        "- Дуэт локальных нейросетей: Qwen-2.5 7B и DeepSeek-R1 7B\n"
        "- Управление рисками (стоп-факторы, скоринг FinOps)\n\n"
        "🐙 GitHub: https://github.com/johnngoan66101996-cmyk/antigravity-quantum-firm\n"
        "Связь: sugatov86@list.ru\n\n"
        "🏷️ <b>Теги:</b> antigravity, нейросети, квантовый ии, торговые роботы, bybit, алготрейдинг, deepseek, qwen"
    )
    send_telegram_message(meta_text)

if __name__ == "__main__":
    main()
