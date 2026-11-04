"""
Send 5-Minute China AI Production Pack & Video to Telegram for Moderation (v9.0.0-OMEGA)
"""

import os
import requests
from pathlib import Path

TOKEN = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
CHAT_ID = "8558082021"

ARTIFACTS_DIR = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
VIDEO_FILE = Path(r"C:\Users\sugat\OneDrive\Desktop\china_ai_revolution_5min.mp4")

SCENES = [
    (
        ARTIFACTS_DIR / "quantum_ai_datacenter_shanghai_1793777422779.jpg",
        "🇨🇳 *СЦЕНА 1: КИТАЙСКИЙ ПРОРЫВ В OPEN-SOURCE (00:00–00:45)*\nПанорама ночного Шанхая и Шэньчжэня, циклопический дата-центр квантовых вычислений DeepSeek и Qwen с жидкостным охлаждением."
    ),
    (
        ARTIFACTS_DIR / "deepseek_r1_quantum_core_1793777429106.jpg",
        "🧠 *СЦЕНА 2: АРХИТЕКТУРНОЕ ЯДРО DEEPSEEK-R1 (00:45–01:45)*\nВизуализация Multi-Head Latent Attention (MLA), Mixture-of-Experts (MoE 671B) и чистого Reinforcement Learning."
    ),
    (
        ARTIFACTS_DIR / "quantum_ai_developer_workstation_1793777437480.jpg",
        "💻 *СЦЕНА 3: QWEN-2.5 CODER 32B + CLAUDE CODE (01:45–02:45)*\nАвтономная терминальная разработка без подписок. Прозрачный PowerShell Matrix HUD, генерация микросервисов."
    ),
    (
        ARTIFACTS_DIR / "quantum_trading_desk_shenzhen_1793777483857.jpg",
        "📈 *СЦЕНА 4: КВАНТОВЫЙ L2 ТРЕЙДИНГ В ШЭНЬЧЖЭНЕ (02:45–03:45)*\nМикросекундный анализ плотностей стакана Bybit UTA по модели Авельянеда-Стоикова со стоп-лоссом 25 bps."
    ),
    (
        ARTIFACTS_DIR / "quantum_ai_outro_branding_1793777483308.jpg",
        "⚡ *СЦЕНА 5: ТИТУЛЬНЫЙ БРЕНДИНГ И АГЕНТНЫЙ ВОРОНКА (03:45–05:00)*\nКвантовая плазменная сфера, интеграция с Telegram-ботом @torgovii8_bot и призыв к подписке."
    )
]

def main():
    print("[*] 1. Отправка 5 фотореалистичных сцен 8K...")
    for img_path, caption in SCENES:
        if img_path.exists():
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            with open(img_path, "rb") as f:
                r = requests.post(url, data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"}, files={"photo": f}, timeout=30)
                print(f"[+] Сцена {img_path.name[:25]}... отправлена: HTTP {r.status_code}")

    print("[*] 2. Отправка метаданных и сценария на модерацию...")
    text_meta = (
        "📋 *ПРОИЗВОДСТВЕННЫЙ ПАКЕТ НА МОДЕРАЦИЮ (5 МИНУТ)*\n\n"
        "📺 *Канал:* «Квантовый ИИ: Claude Code, GPT & Нейросети» (ID: 74595918)\n"
        "🎬 *Название:* `КВАНТОВЫЙ ИИ: Китайская Революция Open-Source — DeepSeek-R1, Qwen-2.5 Coder и Агенты Нового Поколения`\n"
        "⏱ *Хронометраж:* ровно 5 минут (300 секунд)\n"
        "🎯 *Категория:* Технологии и интернет (12+)\n"
        "🏷 *Теги:* deepseek, deepseek r1, qwen, qwen 2.5 coder, claude code, нейросети, квантовый ии, алгоритмический трейдинг, ollama, vllm\n\n"
        "⚡ *Анализ трендов канала:* По статистике канала максимальное удержание и просмотры (388+) показывают темы ИИ-редакторов кода и автономных инструментов. Китайский технологический скачок (DeepSeek + Qwen) — самая острая и виральная тема 2026 года."
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text_meta, "parse_mode": "Markdown"}, timeout=20)

    print("[*] 3. Отправка 5-минутного видеофайла (27.2 МБ)...")
    if VIDEO_FILE.exists():
        url_video = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
        with open(VIDEO_FILE, "rb") as f:
            r = requests.post(
                url_video,
                data={
                    "chat_id": CHAT_ID,
                    "caption": "🎥 *ГОТОВЫЙ 5-МИНУТНЫЙ РОЛИК (300 СЕК)*\nТема: Китайская революция Open-Source ИИ (DeepSeek, Qwen 2.5, Квантовый трейдинг).\nГотов к загрузке на Rutube после модерации.",
                    "parse_mode": "Markdown",
                    "supports_streaming": True
                },
                files={"video": f},
                timeout=120
            )
            print(f"[+] 5-минутное видео отправлено: HTTP {r.status_code}")

if __name__ == "__main__":
    main()
