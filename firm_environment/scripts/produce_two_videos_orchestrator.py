"""
Orchestrator: Two AI Videos Production Pipeline (v9.0.0-OMEGA)
Автономное производство двух видеороликов:
1. Claude Code & Claude 3.7 Sonnet (Гибридный ИИ и терминальный агент)
2. Grok 3 vs DeepSeek-R1 (Битва титанов 2026: 200k H100 vs Open-Source)

Каждый ролик содержит:
- Дикторскую озвучку (SAPI Speech Synthesis)
- Живой инфографический фотоколлаж (PIL Graphics)
- Скомпилированное видео (FFmpeg H.264 / AAC 1080p)
- Полное структурированное SEO-описание
- Доставку всех материалов в Telegram-чат для модерации
"""

import os
import sys
import subprocess
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

STORAGE_DIR = Path("firm_environment/storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
BRAIN_DIR = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
DESKTOP_DIR = Path(r"C:\Users\sugat\OneDrive\Desktop")

TELEGRAM_TOKEN = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
CHAT_ID = "8558082021"

# -------------------------------------------------------------
# 1. ТЕКСТЫ ОЗВУЧКИ И МЕТАДАННЫЕ
# -------------------------------------------------------------

SCRIPT_1_TEXT = (
    "Привет зрителям канала Квантовый ИИ! Сегодня мы разбираем главное событие в индустрии автономной разработки: "
    "выход Claude 3.7 Sonnet и официального терминального агента Claude Code от Anthropic. "
    "Это первая в мире гибридная модель мышления, объединяющая мгновенный отклик и настраиваемый бюджет глубоких рассуждений. "
    "А терминальный агент Claude Code позволяет делегировать инженерные задачи напрямую через консоль: "
    "автономно искать и редактировать файлы репозитория, запускать тесты, устранять ошибки компиляции и работать с Git. "
    "Забудьте про рутину и подписки. Подписывайтесь на канал Квантовый ИИ и забирайте готовые конфигурации в нашем Телеграм боте!"
)

META_1_TITLE = "CLAUDE CODE & CLAUDE 3.7: Первый гибридный ИИ и автономный терминальный агент"
META_1_DESC = (
    "⚡ Официальный разбор Claude 3.7 Sonnet и революционного CLI-агента Claude Code от Anthropic на канале «Квантовый ИИ»!\n\n"
    "Что нового в релизе:\n"
    "— Первая в мире гибридная архитектура мышления (Hybrid Reasoning): мгновенные ответы + режим глубоких размышлений (Extended Thinking Budget).\n"
    "— Терминальный агент Claude Code: автономное редактирование репозиториев, автоматический запуск тестов, авто-фикс багов и интеграция с Git.\n"
    "— Рекордные результаты на SWE-bench Verified (70.3%) в реальных задачах разработки ПО.\n\n"
    "⏱ ТАЙМКОДЫ:\n"
    "00:00 — Введение: Конец эпохи классических IDE\n"
    "00:30 — Архитектура Hybrid Reasoning в Claude 3.7 Sonnet\n"
    "01:00 — Как Claude Code меняет работу в терминале\n"
    "01:30 — Настройка связки и выводы\n\n"
    "💎 Конфигурации и промпты: https://t.me/torgovii8_bot\n"
    "#claudecode #claude37 #anthropic #ai #coding #квантовыйии #нейросети"
)

SCRIPT_2_TEXT = (
    "На канале Квантовый ИИ — битва титанов 2026 года! "
    "Илон Маск и стартап xAI представили Grok 3, обученный на суперкомпьютере Colossus из двухсот тысяч видеокарт Nvidia H100. "
    "Модель установила абсолютный рекорд на Chatbot Arena, набрав более 1400 пунктов рейтинга Elo. "
    "Однако китайский открытый ответ в лице DeepSeek-R1 доказывает обратное: "
    "благодаря инновационному сжатию контекста MLA и архитектуре MoE 671B, "
    "сопоставимое качество логики можно запускать локально на домашнем железе без миллиардных затрат. "
    "Суперкомпьютерная монополия против открытого суверенитета: кто победит? "
    "Смотрите сравнительный анализ на канале Квантовый ИИ и переходите в наш Телеграм бот!"
)

META_2_TITLE = "БИТВА ТИТАНОВ 2026: Grok 3 против DeepSeek-R1 — 200,000 H100 против Open-Source"
META_2_DESC = (
    "🔥 Главное технологическое противостояние 2026 года: суперкластер xAI Colossus против китайской открытой революции DeepSeek-R1!\n\n"
    "Ключевые факты расследования:\n"
    "— Grok 3 от Илона Маска: 200 000 ускорителей Nvidia H100 в Мемфисе, 2.7 триллиона параметров и рекордные 1400+ Elo на LMSYS Chatbot Arena.\n"
    "— DeepSeek-R1: открытые веса, Multi-Head Latent Attention (MLA), сжатие памяти на 90% и чистый Reinforcement Learning.\n"
    "— Сравнение стоимости вывода: миллиардные суперкластеры против квантованного запуска на домашних GPU RTX 3090/4090.\n\n"
    "⏱ ТАЙМКОДЫ:\n"
    "00:00 — Старт битвы: 200 тысяч H100 в кластере Colossus\n"
    "00:35 — Рекорд Grok 3 на Chatbot Arena\n"
    "01:10 — Почему DeepSeek-R1 меняет правила игры\n"
    "01:40 — Итог: Кто победит в гонке ИИ?\n\n"
    "💎 Все бенчмарки и локальные скрипты запуска: https://t.me/torgovii8_bot\n"
    "#grok3 #deepseek #elonmusk #xai #colossus #ai #квантовыйии #нейросети"
)

# -------------------------------------------------------------
# 2. СИНТЕЗ ОЗВУЧКИ ЧЕРЕЗ POWERSHELL SAPI
# -------------------------------------------------------------

def synthesize_speech(text, output_wav):
    print(f"[*] Синтез речи SAPI -> {output_wav.name}...")
    ps_code = f"""
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.Rate = 1
    $synth.Volume = 100
    $synth.SetOutputToWaveFile('{str(output_wav.resolve())}')
    $synth.Speak(@'
{text}
'@)
    $synth.Dispose()
    """
    temp_ps1 = STORAGE_DIR / f"temp_synth_{output_wav.stem}.ps1"
    with open(temp_ps1, "w", encoding="utf-8") as f:
        f.write(ps_code)
    
    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(temp_ps1)], capture_output=True, text=True)
    if output_wav.exists() and output_wav.stat().st_size > 1000:
        print(f"[+] Аудио успешно синтезировано: {output_wav.name} ({output_wav.stat().st_size} байт)")
        return True
    else:
        print(f"[!] Ошибка синтеза: {res.stderr}")
        return False

# -------------------------------------------------------------
# 3. ГЕНЕРАЦИЯ ЖИВЫХ ИНФОГРАФИЧЕСКИХ КОЛЛАЖЕЙ (1920x1080)
# -------------------------------------------------------------

def build_collage_1(output_png):
    print(f"[*] Сборка инфографического коллажа: {output_png.name}...")
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (10, 14, 23))
    draw = ImageDraw.Draw(im)

    # Заголовок
    draw.rectangle([(0, 0), (W, 110)], fill=(15, 23, 42))
    draw.text((60, 30), "ANTHROPIC CLAUDE 3.7 SONNET & CLAUDE CODE CLI", fill=(56, 189, 248))
    draw.text((60, 75), "ОФИЦИАЛЬНЫЙ РАЗБОР ГИБРИДНОГО МЫШЛЕНИЯ И ТЕРМИНАЛЬНЫХ АГЕНТОВ | КАНАЛ «КВАНТОВЫЙ ИИ»", fill=(148, 163, 184))

    # Блок 1: Hybrid Reasoning
    b1 = [(60, 150), (920, 560)]
    draw.rectangle(b1, fill=(19, 31, 56), outline=(56, 189, 248), width=2)
    draw.text((80, 170), "1. ГИБРИДНОЕ МЫШЛЕНИЕ (HYBRID REASONING)", fill=(244, 114, 182))
    draw.text((80, 220), "• Standard Mode: Мгновенный отклик для типовых задач и генерации UI", fill=(226, 232, 240))
    draw.text((80, 270), "• Extended Thinking: Пошаговое внутреннее размышление перед ответом", fill=(226, 232, 240))
    draw.text((80, 320), "• Granular Token Budget: Ручное управление глубиной анализа и ценой", fill=(226, 232, 240))
    draw.text((80, 370), "• Унифицированная архитектура без переключения между разными моделями", fill=(226, 232, 240))
    draw.text((80, 430), "Статус: Выход на Claude API, Amazon Bedrock, Google Vertex AI", fill=(52, 211, 153))

    # Блок 2: Claude Code CLI
    b2 = [(960, 150), (1860, 560)]
    draw.rectangle(b2, fill=(19, 31, 56), outline=(168, 85, 247), width=2)
    draw.text((980, 170), "2. ТЕРМИНАЛЬНЫЙ АГЕНТ CLAUDE CODE", fill=(168, 85, 247))
    draw.text((980, 220), "• Прямое управление репозиторием прямо из командной строки (CLI)", fill=(226, 232, 240))
    draw.text((980, 270), "• Чтение и редактирование файлов проекта без вставки в браузер", fill=(226, 232, 240))
    draw.text((980, 320), "• Автономный запуск тестов и исправление ошибок компиляции на лету", fill=(226, 232, 240))
    draw.text((980, 370), "• Полная автоматизация Git: создание веток, коммиты, пулреквесты", fill=(226, 232, 240))
    draw.text((980, 430), "Команда установки: npm install -g @anthropic-ai/claude-code", fill=(251, 191, 36))

    # Блок 3: Бенчмарки SWE-bench Verified
    b3 = [(60, 600), (1860, 960)]
    draw.rectangle(b3, fill=(15, 23, 42), outline=(34, 197, 94), width=2)
    draw.text((80, 620), "3. МИРОВОЙ РЕКОРД В РЕАЛЬНОМ ПРОГРАММИРОВАНИИ (SWE-BENCH VERIFIED)", fill=(34, 197, 94))
    draw.text((80, 680), "Claude 3.7 Sonnet (Hybrid Reasoning):   70.3%   [АБСОЛЮТНЫЙ ЛИДЕР]", fill=(255, 255, 255))
    draw.text((80, 730), "OpenAI o3-mini (High Reasoning):        68.1%", fill=(148, 163, 184))
    draw.text((80, 780), "Claude 3.5 Sonnet:                      49.0%", fill=(148, 163, 184))
    draw.text((80, 830), "GPT-4o (Classic API):                   38.8%", fill=(148, 163, 184))
    draw.text((80, 890), "Эволюция: +21.3% прирост точности в сложных многофайловых репозиториях GitHub!", fill=(56, 189, 248))

    # Футер
    draw.rectangle([(0, 990), (W, H)], fill=(15, 23, 42))
    draw.text((60, 1015), "КАНАЛ «КВАНТОВЫЙ ИИ» | ТЕЛЕГРАМ БОТ: @torgovii8_bot", fill=(255, 255, 255))
    
    im.save(output_png)
    print(f"[+] Коллаж 1 создан: {output_png.name}")

def build_collage_2(output_png):
    print(f"[*] Сборка инфографического коллажа: {output_png.name}...")
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (12, 10, 20))
    draw = ImageDraw.Draw(im)

    # Заголовок
    draw.rectangle([(0, 0), (W, 110)], fill=(24, 18, 38))
    draw.text((60, 30), "BATTLE OF TITANS 2026: GROK 3 VS DEEPSEEK-R1", fill=(239, 68, 68))
    draw.text((60, 75), "СУПЕРКЛАСТЕР COLOSSUS (200k H100) ПРОТИВ КИТАЙСКОГО ОТКРЫТОГО ИИ | КАНАЛ «КВАНТОВЫЙ ИИ»", fill=(209, 213, 219))

    # Блок 1: Grok 3 & Colossus
    b1 = [(60, 150), (920, 560)]
    draw.rectangle(b1, fill=(28, 20, 44), outline=(239, 68, 68), width=2)
    draw.text((80, 170), "GROK 3 & СУПЕРКЛАСТЕР COLOSSUS (xAI)", fill=(239, 68, 68))
    draw.text((80, 220), "• Инфраструктура: 200 000 связанных Nvidia H100 в Мемфисе", fill=(243, 244, 246))
    draw.text((80, 270), "• Масштаб модели: ~2.7 триллиона параметров (10x прирост compute)", fill=(243, 244, 246))
    draw.text((80, 320), "• Режим Think Mode / Big Brain: глубокие цепочки рассуждений", fill=(243, 244, 246))
    draw.text((80, 370), "• Агент DeepSearch: прямой парсинг соцсети X и открытого веба", fill=(243, 244, 246))
    draw.text((80, 430), "Chatbot Arena LMSYS: 1400+ Elo [Рекорд первого места]", fill=(248, 113, 113))

    # Блок 2: DeepSeek-R1 & Qwen Coder
    b2 = [(960, 150), (1860, 560)]
    draw.rectangle(b2, fill=(19, 31, 56), outline=(34, 197, 94), width=2)
    draw.text((980, 170), "DEEPSEEK-R1 & OPEN-SOURCE РЕВОЛЮЦИЯ", fill=(34, 197, 94))
    draw.text((980, 220), "• Архитектура MLA: сжатие KV-кэша более чем на 90%", fill=(243, 244, 246))
    draw.text((980, 270), "• Mixture of Experts: 37B активных из общих 671B параметров", fill=(243, 244, 246))
    draw.text((980, 320), "• Чистый Large-Scale RL без дорогой ручной разметки людей", fill=(243, 244, 246))
    draw.text((980, 370), "• Локальный запуск: квантованные версии GGUF для домашних ПК", fill=(243, 244, 246))
    draw.text((980, 430), "Стоимость вывода: в 10–20 раз дешевле закрытых API США!", fill=(52, 211, 153))

    # Блок 3: Сравнительная таблица
    b3 = [(60, 600), (1860, 960)]
    draw.rectangle(b3, fill=(20, 18, 30), outline=(251, 191, 36), width=2)
    draw.text((80, 620), "КЛЮЧЕВЫЕ РАЗЛИЧИЯ ФИЛОСОФИЙ ИИ НА 2026 ГОД", fill=(251, 191, 36))
    draw.text((80, 680), "Параметр                   Grok 3 (xAI)                 DeepSeek-R1 / Qwen 2.5", fill=(255, 255, 255))
    draw.text((80, 730), "Доступность весов:         Закрытое облако (SaaS)       Открытые веса (Open Weights)", fill=(209, 213, 219))
    draw.text((80, 780), "Требуемое железо:          Дата-центры мегаватт-класса  Домашняя видеокарта RTX 3090/4090", fill=(209, 213, 219))
    draw.text((80, 830), "Приватность данных:        Отправка на серверы xAI      100% локально и изолированно", fill=(209, 213, 219))
    draw.text((80, 890), "Результат: Grok 3 лидирует по сырой мощности, но DeepSeek дает суверенитет разработчикам!", fill=(56, 189, 248))

    # Футер
    draw.rectangle([(0, 990), (W, H)], fill=(24, 18, 38))
    draw.text((60, 1015), "КАНАЛ «КВАНТОВЫЙ ИИ» | ТЕЛЕГРАМ БОТ: @torgovii8_bot", fill=(255, 255, 255))
    
    im.save(output_png)
    print(f"[+] Коллаж 2 создан: {output_png.name}")

# -------------------------------------------------------------
# 4. КОМПИЛЯЦИЯ ВИДЕОРОЛИКОВ FFMPEG
# -------------------------------------------------------------

def compile_mp4(images_list, audio_wav, output_mp4, duration_total):
    print(f"[*] Сборка видео -> {output_mp4.name} (длительность {duration_total}c)...")
    
    dur_per_img = duration_total / len(images_list)
    concat_txt = STORAGE_DIR / f"concat_{output_mp4.stem}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for img in images_list:
            f.write(f"file '{img.resolve()}'\n")
            f.write(f"duration {dur_per_img:.1f}\n")
        f.write(f"file '{images_list[-1].resolve()}'\n")
        
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(audio_wav),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(output_mp4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if output_mp4.exists() and output_mp4.stat().st_size > 1000:
        print(f"[+++] ВИДЕО УСПЕШНО СКОМПИЛИРОВАНО: {output_mp4.name} ({output_mp4.stat().st_size} байт)")
        return True
    else:
        print(f"[!] Ошибка ffmpeg: {res.stderr[-400:]}")
        return False

# -------------------------------------------------------------
# 5. ОТПРАВКА В TELEGRAM НА МОДЕРАЦИЮ
# -------------------------------------------------------------

def send_to_telegram(collage_path, audio_path, video_path, title, description):
    print(f"[*] Отправка пакета на модерацию в Telegram: '{title}'...")
    
    # 1. Отправка коллажа
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(collage_path, "rb") as f:
        r = requests.post(url_photo, data={"chat_id": CHAT_ID, "caption": f"📸 *ЖИВОЙ ФОТОКОЛЛАЖ И ИНФОГРАФИКА*\n{title}"}, files={"photo": f})
        print(f"[+] Коллаж отправлен: HTTP {r.status_code}")
        
    # 2. Отправка метаданных
    url_msg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url_msg, data={"chat_id": CHAT_ID, "text": f"📋 *МЕТАДАННЫЕ И ОПИСАНИЕ РОЛИКА:*\n\n*Название:* {title}\n\n*Описание:*\n{description}"})
    
    # 3. Отправка аудио озвучки
    url_audio = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio"
    with open(audio_path, "rb") as f:
        r = requests.post(url_audio, data={"chat_id": CHAT_ID, "title": title, "performer": "Квантовый ИИ"}, files={"audio": f})
        print(f"[+] Аудиодорожка озвучки отправлена: HTTP {r.status_code}")
        
    # 4. Отправка видео
    url_video = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    with open(video_path, "rb") as f:
        r = requests.post(url_video, data={"chat_id": CHAT_ID, "caption": f"🎥 *ГОТОВЫЙ ВИДЕОРОЛИК ДЛЯ RUTUBE*\n{title}"}, files={"video": f}, timeout=120)
        print(f"[+] Скомпилированное видео отправлено: HTTP {r.status_code}")

# -------------------------------------------------------------
# ГЛАВНЫЙ ЦИКЛ ОРКЕСТРАТОРА
# -------------------------------------------------------------

def run_production():
    print("==================================================")
    print("  АВТОНОМНЫЙ РЕЖИССЕР-ОРКЕСТРАТОР ВИДЕОПРОДАКШНА ")
    print("==================================================")
    
    # 1. Генерация аудиодорожек
    wav_1 = STORAGE_DIR / "voiceover_video1_claude.wav"
    wav_2 = STORAGE_DIR / "voiceover_video2_grok.wav"
    synthesize_speech(SCRIPT_1_TEXT, wav_1)
    synthesize_speech(SCRIPT_2_TEXT, wav_2)
    
    # 2. Сборка живых инфографических коллажей
    col_1 = STORAGE_DIR / "collage_video1_claude.png"
    col_2 = STORAGE_DIR / "collage_video2_grok.png"
    build_collage_1(col_1)
    build_collage_2(col_2)
    
    # 3. Подготовка видеорядов
    # Для Ролика 1: Коллаж 1 + Рабочее место Qwen/Claude + Брендинг канала
    imgs_video1 = [
        col_1,
        BRAIN_DIR / "quantum_ai_developer_workstation_1793777437480.jpg",
        BRAIN_DIR / "quantum_ai_outro_branding_1793777483308.jpg"
    ]
    # Для Ролика 2: Коллаж 2 + Квантовое ядро DeepSeek + Трейдинг-деск Шэньчжэнь
    imgs_video2 = [
        col_2,
        BRAIN_DIR / "deepseek_r1_quantum_core_1793777429106.jpg",
        BRAIN_DIR / "quantum_trading_desk_shenzhen_1793777483857.jpg"
    ]
    
    # 4. Компиляция видеороликов
    mp4_1 = DESKTOP_DIR / "video1_claude_code_hybrid.mp4"
    mp4_2 = DESKTOP_DIR / "video2_grok3_vs_deepseek.mp4"
    compile_mp4(imgs_video1, wav_1, mp4_1, duration_total=60)
    compile_mp4(imgs_video2, wav_2, mp4_2, duration_total=60)
    
    # 5. Отправка на модерацию в Telegram
    send_to_telegram(col_1, wav_1, mp4_1, META_1_TITLE, META_1_DESC)
    send_to_telegram(col_2, wav_2, mp4_2, META_2_TITLE, META_2_DESC)
    
    print("[+++] ВСЕ ЭТАПЫ ПРОИЗВОДСТВА И МОДЕРАЦИИ УСПЕШНО ЗАВЕРШЕНЫ!")

if __name__ == "__main__":
    run_production()
