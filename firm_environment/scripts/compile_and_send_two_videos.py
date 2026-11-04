"""
Compile & Send Two AI Videos to Telegram for Moderation (v9.0.0-OMEGA)
"""

import subprocess
import requests
from pathlib import Path
from PIL import Image, ImageDraw

STORAGE_DIR = Path("firm_environment/storage")
BRAIN_DIR = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
DESKTOP_DIR = Path(r"C:\Users\sugat\OneDrive\Desktop")

TOKEN = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
CHAT_ID = "8558082021"

WAV_1 = STORAGE_DIR / "voiceover1_claude.wav"
WAV_2 = STORAGE_DIR / "voiceover2_grok.wav"

COL_1 = STORAGE_DIR / "collage_video1_claude.png"
COL_2 = STORAGE_DIR / "collage_video2_grok.png"

MP4_1 = DESKTOP_DIR / "video1_claude_code_hybrid.mp4"
MP4_2 = DESKTOP_DIR / "video2_grok3_vs_deepseek.mp4"

def make_collages():
    print("[*] 1. Генерация коллажей 1920x1080...")
    W, H = 1920, 1080
    
    # Коллаж 1: Claude Code
    im1 = Image.new("RGB", (W, H), (10, 15, 26))
    d1 = ImageDraw.Draw(im1)
    d1.rectangle([(0, 0), (W, 110)], fill=(15, 23, 42))
    d1.text((60, 30), "ANTHROPIC CLAUDE 3.7 SONNET & CLAUDE CODE CLI", fill=(56, 189, 248))
    d1.text((60, 75), "ПЕРВЫЙ ГИБРИДНЫЙ ИИ И АВТОНОМНЫЙ ТЕРМИНАЛЬНЫЙ АГЕНТ | КАНАЛ «КВАНТОВЫЙ ИИ»", fill=(148, 163, 184))

    d1.rectangle([(60, 150), (920, 560)], fill=(19, 31, 56), outline=(56, 189, 248), width=2)
    d1.text((80, 170), "1. ГИБРИДНОЕ МЫШЛЕНИЕ (HYBRID REASONING)", fill=(244, 114, 182))
    d1.text((80, 220), "• Standard Mode: Мгновенный отклик для типовых задач и генерации UI", fill=(226, 232, 240))
    d1.text((80, 270), "• Extended Thinking: Пошаговое внутреннее размышление перед ответом", fill=(226, 232, 240))
    d1.text((80, 320), "• Granular Token Budget: Ручное управление глубиной анализа и ценой", fill=(226, 232, 240))
    d1.text((80, 370), "• Единая модель без переключения между разными нейросетями", fill=(226, 232, 240))
    d1.text((80, 430), "Статус: Доступно в Claude API, Amazon Bedrock, Google Vertex AI", fill=(52, 211, 153))

    d1.rectangle([(960, 150), (1860, 560)], fill=(19, 31, 56), outline=(168, 85, 247), width=2)
    d1.text((980, 170), "2. ТЕРМИНАЛЬНЫЙ АГЕНТ CLAUDE CODE", fill=(168, 85, 247))
    d1.text((980, 220), "• Прямое управление репозиторием из командной строки (CLI)", fill=(226, 232, 240))
    d1.text((980, 270), "• Чтение и редактирование файлов проекта без ручного копирования", fill=(226, 232, 240))
    d1.text((980, 320), "• Автономный запуск тестов и исправление ошибок компиляции на лету", fill=(226, 232, 240))
    d1.text((980, 370), "• Полная автоматизация Git: создание веток, коммиты, код-ревью", fill=(226, 232, 240))
    d1.text((980, 430), "Команда установки: npm install -g @anthropic-ai/claude-code", fill=(251, 191, 36))

    d1.rectangle([(60, 600), (1860, 960)], fill=(15, 23, 42), outline=(34, 197, 94), width=2)
    d1.text((80, 620), "3. МИРОВОЙ РЕКОРД В РЕАЛЬНОМ ПРОГРАММИРОВАНИИ (SWE-BENCH VERIFIED)", fill=(34, 197, 94))
    d1.text((80, 680), "Claude 3.7 Sonnet (Hybrid Reasoning):   70.3%   [АБСОЛЮТНЫЙ ЛИДЕР]", fill=(255, 255, 255))
    d1.text((80, 730), "OpenAI o3-mini (High Reasoning):        68.1%", fill=(148, 163, 184))
    d1.text((80, 780), "Claude 3.5 Sonnet:                      49.0%", fill=(148, 163, 184))
    d1.text((80, 830), "GPT-4o (Classic API):                   38.8%", fill=(148, 163, 184))
    d1.text((80, 890), "Эволюция: +21.3% прирост точности в сложных многофайловых репозиториях GitHub!", fill=(56, 189, 248))

    d1.rectangle([(0, 990), (W, H)], fill=(15, 23, 42))
    d1.text((60, 1015), "КАНАЛ «КВАНТОВЫЙ ИИ» | ТЕЛЕГРАМ БОТ: @torgovii8_bot", fill=(255, 255, 255))
    im1.save(COL_1)

    # Коллаж 2: Grok 3 vs DeepSeek
    im2 = Image.new("RGB", (W, H), (12, 10, 20))
    d2 = ImageDraw.Draw(im2)
    d2.rectangle([(0, 0), (W, 110)], fill=(24, 18, 38))
    d2.text((60, 30), "BATTLE OF TITANS 2026: GROK 3 VS DEEPSEEK-R1", fill=(239, 68, 68))
    d2.text((60, 75), "СУПЕРКЛАСТЕР COLOSSUS (200k H100) ПРОТИВ КИТАЙСКОГО ОТКРЫТОГО ИИ | КАНАЛ «КВАНТОВЫЙ ИИ»", fill=(209, 213, 219))

    d2.rectangle([(60, 150), (920, 560)], fill=(28, 20, 44), outline=(239, 68, 68), width=2)
    d2.text((80, 170), "GROK 3 & СУПЕРКЛАСТЕР COLOSSUS (xAI)", fill=(239, 68, 68))
    d2.text((80, 220), "• Инфраструктура: 200 000 связанных Nvidia H100 в Мемфисе", fill=(243, 244, 246))
    d2.text((80, 270), "• Масштаб модели: ~2.7 триллиона параметров (10x прирост compute)", fill=(243, 244, 246))
    d2.text((80, 320), "• Режим Think Mode / Big Brain: глубокие цепочки рассуждений", fill=(243, 244, 246))
    d2.text((80, 370), "• Агент DeepSearch: прямой парсинг соцсети X и открытого веба", fill=(243, 244, 246))
    d2.text((80, 430), "Chatbot Arena LMSYS: 1400+ Elo [Рекорд первого места]", fill=(248, 113, 113))

    d2.rectangle([(960, 150), (1860, 560)], fill=(19, 31, 56), outline=(34, 197, 94), width=2)
    d2.text((980, 170), "DEEPSEEK-R1 & OPEN-SOURCE РЕВОЛЮЦИЯ", fill=(34, 197, 94))
    d2.text((980, 220), "• Архитектура MLA: сжатие KV-кэша более чем на 90%", fill=(243, 244, 246))
    d2.text((980, 270), "• Mixture of Experts: 37B активных из общих 671B параметров", fill=(243, 244, 246))
    d2.text((980, 320), "• Чистый Large-Scale RL без дорогой ручной разметки людей", fill=(243, 244, 246))
    d2.text((980, 370), "• Локальный запуск: квантованные версии GGUF для домашних ПК", fill=(243, 244, 246))
    d2.text((980, 430), "Стоимость вывода: в 10–20 раз дешевле закрытых API США!", fill=(52, 211, 153))

    d2.rectangle([(60, 600), (1860, 960)], fill=(20, 18, 30), outline=(251, 191, 36), width=2)
    d2.text((80, 620), "КЛЮЧЕВЫЕ РАЗЛИЧИЯ ФИЛОСОФИЙ ИИ НА 2026 ГОД", fill=(251, 191, 36))
    d2.text((80, 680), "Параметр                   Grok 3 (xAI)                 DeepSeek-R1 / Qwen 2.5", fill=(255, 255, 255))
    d2.text((80, 730), "Доступность весов:         Закрытое облако (SaaS)       Открытые веса (Open Weights)", fill=(209, 213, 219))
    d2.text((80, 780), "Требуемое железо:          Дата-центры мегаватт-класса  Домашняя видеокарта RTX 3090/4090", fill=(209, 213, 219))
    d2.text((80, 830), "Приватность данных:        Отправка на серверы xAI      100% локально и изолированно", fill=(209, 213, 219))
    d2.text((80, 890), "Результат: Grok 3 лидирует по сырой мощности, но DeepSeek дает суверенитет разработчикам!", fill=(56, 189, 248))

    d2.rectangle([(0, 990), (W, H)], fill=(24, 18, 38))
    d2.text((60, 1015), "КАНАЛ «КВАНТОВЫЙ ИИ» | ТЕЛЕГРАМ БОТ: @torgovii8_bot", fill=(255, 255, 255))
    im2.save(COL_2)
    print("[+] Коллажи 1 и 2 успешно сохранены!")

def normalize_image(src_path, dst_path):
    with Image.open(src_path) as img:
        img = img.convert("RGB")
        # Resize preserving aspect ratio or fill 1920x1080
        target = Image.new("RGB", (1920, 1080), (0, 0, 0))
        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        offset = ((1920 - img.width) // 2, (1080 - img.height) // 2)
        target.paste(img, offset)
        target.save(dst_path, "PNG")

def compile_videos():
    print("[*] 2. Нормализация кадров в единый формат PNG 1920x1080...")
    
    # Видео 1 кадры
    f1_1 = STORAGE_DIR / "v1_frame1.png"
    f1_2 = STORAGE_DIR / "v1_frame2.png"
    f1_3 = STORAGE_DIR / "v1_frame3.png"
    normalize_image(COL_1, f1_1)
    normalize_image(BRAIN_DIR / "quantum_ai_developer_workstation_1793777437480.jpg", f1_2)
    normalize_image(BRAIN_DIR / "quantum_ai_outro_branding_1793777483308.jpg", f1_3)

    # Видео 2 кадры
    f2_1 = STORAGE_DIR / "v2_frame1.png"
    f2_2 = STORAGE_DIR / "v2_frame2.png"
    f2_3 = STORAGE_DIR / "v2_frame3.png"
    normalize_image(COL_2, f2_1)
    normalize_image(BRAIN_DIR / "deepseek_r1_quantum_core_1793777429106.jpg", f2_2)
    normalize_image(BRAIN_DIR / "quantum_trading_desk_shenzhen_1793777483857.jpg", f2_3)

    print("[*] Компиляция двух видеороликов через FFmpeg...")
    
    # Видео 1: 50.4 сек. 3 кадра: f1_1 (20с), f1_2 (15с), f1_3 (15.4с)
    c1 = STORAGE_DIR / "concat_v1.txt"
    with open(c1, "w", encoding="utf-8") as f:
        f.write(f"file '{f1_1.resolve()}'\nduration 20\n")
        f.write(f"file '{f1_2.resolve()}'\nduration 15\n")
        f.write(f"file '{f1_3.resolve()}'\nduration 16\n")
        f.write(f"file '{f1_3.resolve()}'\n")
        
    cmd1 = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(c1),
        "-i", str(WAV_1),
        "-f", "lavfi", "-i", "sine=frequency=50:duration=51",
        "-filter_complex", "[1:a]volume=1.0[a1];[2:a]volume=0.15[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-r", "30", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(MP4_1)
    ]
    subprocess.run(cmd1, check=True)
    print(f"[+] Видео 1 готово: {MP4_1.name} ({MP4_1.stat().st_size} байт)")

    # Видео 2: 55.8 сек. 3 кадра: f2_1 (22с), f2_2 (17с), f2_3 (17с)
    c2 = STORAGE_DIR / "concat_v2.txt"
    with open(c2, "w", encoding="utf-8") as f:
        f.write(f"file '{f2_1.resolve()}'\nduration 22\n")
        f.write(f"file '{f2_2.resolve()}'\nduration 17\n")
        f.write(f"file '{f2_3.resolve()}'\nduration 17\n")
        f.write(f"file '{f2_3.resolve()}'\n")

    cmd2 = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(c2),
        "-i", str(WAV_2),
        "-f", "lavfi", "-i", "sine=frequency=50:duration=56",
        "-filter_complex", "[1:a]volume=1.0[a1];[2:a]volume=0.15[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-r", "30", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(MP4_2)
    ]
    subprocess.run(cmd2, check=True)
    print(f"[+] Видео 2 готово: {MP4_2.name} ({MP4_2.stat().st_size} байт)")

def deliver_to_telegram():
    print("[*] 3. Отправка двух комплектов в Telegram на рассмотрение...")
    
    # ПАКЕТ 1: Claude Code
    desc_1 = (
        "🚀 РОЛИК 1: CLAUDE CODE & CLAUDE 3.7 SONNET\n\n"
        "Тема: Первый гибридный ИИ (Hybrid Reasoning) и автономный терминальный агент разработчика Claude Code.\n"
        "Хронометраж: 50.4 сек | 1080p 30fps\n"
        "Озвучка: SAPI Speech Synthesizer с кибернетическим саундтреком.\n"
        "Коллаж: Инфографика архитектуры, SWE-bench Verified (70.3%) и CLI-команд."
    )
    with open(COL_1, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={"chat_id": CHAT_ID, "caption": desc_1}, files={"photo": f})
    with open(WAV_1, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendAudio", data={"chat_id": CHAT_ID, "title": "Озвучка: Claude Code & 3.7", "performer": "Квантовый ИИ"}, files={"audio": f})
    with open(MP4_1, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo", data={"chat_id": CHAT_ID, "caption": "🎥 Видео 1: Claude Code & Claude 3.7 Sonnet (Готово к публикации)"}, files={"video": f}, timeout=120)
    print("[+] Комплект 1 отправлен в Telegram!")

    # ПАКЕТ 2: Grok 3 vs DeepSeek-R1
    desc_2 = (
        "🔥 РОЛИК 2: БИТВА ТИТАНОВ 2026: GROK 3 ПРОТИВ DEEPSEEK-R1\n\n"
        "Тема: Суперкластер Colossus (200,000 H100) Илона Маска против открытой архитектуры DeepSeek-R1 и Qwen 2.5.\n"
        "Хронометраж: 55.8 сек | 1080p 30fps\n"
        "Озвучка: SAPI Speech Synthesizer с саб-басовым дроном.\n"
        "Коллаж: Сравнение философий ИИ, рейтинг Chatbot Arena (1400+ Elo) и локальный запуск."
    )
    with open(COL_2, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={"chat_id": CHAT_ID, "caption": desc_2}, files={"photo": f})
    with open(WAV_2, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendAudio", data={"chat_id": CHAT_ID, "title": "Озвучка: Grok 3 vs DeepSeek", "performer": "Квантовый ИИ"}, files={"audio": f})
    with open(MP4_2, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo", data={"chat_id": CHAT_ID, "caption": "🎥 Видео 2: Grok 3 vs DeepSeek-R1 (Готово к публикации)"}, files={"video": f}, timeout=120)
    print("[+] Комплект 2 отправлен в Telegram!")

if __name__ == "__main__":
    make_collages()
    compile_videos()
    deliver_to_telegram()
    print("[+++] ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ В ПОЛНОМ ОБЪЕМЕ!")
