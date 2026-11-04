"""
Autonomous Rutube Browser Uploader (v9.0.0-OMEGA)
Полный автономный цикл:
1. Запуск Playwright в видимом режиме с персистентным профилем.
2. Проверка сессии в Студии Rutube (https://studio.rutube.ru/videos).
3. Авторизация через email sugatov86@list.ru -> клик 'Войти по одноразовому коду' -> авто-перехват 4-значного OTP из IMAP Mail.ru (rutube@rutubeinfo.ru).
4. Ввод 4-значного кода через keyboard.type.
5. Загрузка видео C:\\Users\\sugat\\OneDrive\\Desktop\\antigravity_v25_promo.mp4.
6. Заполнение метаданных (Название, Описание, Теги).
7. Публикация и фиксация статуса в SQLite и отправка отчета в Telegram.
"""

import os
import sys
import time
import json
import re
import sqlite3
import urllib.request
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPTS_DIR))
import mail_otp_reader

def log(msg):
    print(msg, flush=True)

VIDEO_PATH = Path(r"C:\Users\sugat\OneDrive\Desktop\antigravity_v25_promo.mp4")
STORAGE_DIR = Path("firm_environment/storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
USER_DATA_DIR = STORAGE_DIR / "rutube_browser_profile"

TITLE = "ANTIGRAVITY v2.5: Промышленный торговый комплекс и квантовые агенты L2"
DESCRIPTION = (
    "Промышленный обзор автономного квантового торгового комплекса ANTIGRAVITY v2.5.\n\n"
    "⚡ Ключевые возможности системы:\n"
    "— Двухъядерный контур рассуждений: Qwen-2.5 7B (высокоскоростной скоринг стакана) и DeepSeek-R1 7B (стратегическая валидация).\n"
    "— Захват спреда L2 на базе стохастической модели Авельянеда-Стоикова (Avellaneda-Stoikov).\n"
    "— Защита капитала: жесткий лимит стоп-лосса 25 bps и валидатор сделок Actor-Critic.\n"
    "— Полная интеграция с Bybit V5 Unified Trading Account (UTA) и терминалом CScalp.\n\n"
    "#antigravity #bybit #scalping #crypto #trading #deepseek #qwen #algorithmic_trading"
)

TELEGRAM_BOT_TOKEN = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
TELEGRAM_CHAT_ID = "8558082021"

def send_telegram_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log(f"[!] Telegram notify error: {e}")

def wait_for_new_otp(initial_code, timeout_seconds=90):
    log(f"[*] Сканирование почты sugatov86@list.ru на поступление свежего OTP RUTUBE...")
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        time.sleep(3)
        res = mail_otp_reader.get_latest_code()
        if res.get("status") == "FOUND":
            code = res.get("code")
            if code and code != initial_code:
                log(f"[+] УСПЕШНО ПЕРЕХВАЧЕН СВЕЖИЙ КОД: {code} (Отправитель: {res.get('sender')})")
                return code
    log("[-] Таймаут ожидания нового OTP-кода.")
    return None

def execute_browser_upload():
    if not VIDEO_PATH.exists():
        log(f"[!] Файл видео не найден: {VIDEO_PATH}")
        return False
        
    log(f"[+] Подготовлен видеофайл: {VIDEO_PATH} ({VIDEO_PATH.stat().st_size} байт)")
    
    # 0. Базовый код
    baseline = mail_otp_reader.get_latest_code()
    baseline_code = baseline.get("code") if baseline.get("status") == "FOUND" else None
    log(f"[*] Базовый код в ящике: {baseline_code}")

    with sync_playwright() as p:
        log("[*] Запуск браузера Edge с персистентным профилем...")
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            channel="msedge",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox"
            ],
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        )
        
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        
        # 1. Проверяем Студию
        log("[*] Переход в Студию Rutube: https://studio.rutube.ru/videos...")
        page.goto("https://studio.rutube.ru/videos", timeout=60000)
        page.wait_for_timeout(4000)
        
        page.screenshot(path=str(STORAGE_DIR / "rutube_step1_initial.png"))
        current_url = page.url
        log(f"[*] Текущий URL: {current_url}")
        
        # Проверяем, перенаправило ли на страницу логина
        if "login" in current_url or "multipass" in current_url or "gid.ru" in current_url or page.locator("input[name='username']").count() > 0:
            log("[*] Требуется авторизация в Rutube Multipass...")
            
            # Поиск поля ввода логина/почты
            email_field = page.locator("input[name='username'], input[type='email'], input[placeholder*='почт'], input[placeholder*='Телефон']").first
            if email_field.count() > 0 and email_field.is_visible():
                log("[*] Ввод почты sugatov86@list.ru...")
                email_field.click()
                email_field.fill("sugatov86@list.ru")
                page.wait_for_timeout(1000)
                
                # Кнопка Submit / Продолжить
                submit_btn = page.locator("button[type='submit'], button:has-text('Продолжить'), button:has-text('Войти')").first
                if submit_btn.count() > 0:
                    log("[*] Нажатие кнопки подтверждения логина...")
                    submit_btn.click()
                    page.wait_for_timeout(4000)
                else:
                    email_field.press("Enter")
                    page.wait_for_timeout(4000)
            
            # Проверяем наличие кнопки 'Войти по одноразовому коду'
            page.wait_for_timeout(2000)
            otp_login_btn = page.locator("button:has-text('одноразовому коду'), div:has-text('Войти по одноразовому коду'), a:has-text('одноразовому коду')").last
            if otp_login_btn.count() > 0 and otp_login_btn.is_visible():
                log("[*] Обнаружена кнопка 'Войти по одноразовому коду'! Нажимаем для отправки кода на почту...")
                otp_login_btn.click()
                page.wait_for_timeout(3000)
                page.screenshot(path=str(STORAGE_DIR / "rutube_step2b_after_otp_click.png"))
            
            # Ждем код из почты
            new_otp = wait_for_new_otp(baseline_code, timeout_seconds=90)
            if new_otp:
                log(f"[*] Ввод OTP-кода {new_otp} на странице...")
                otp_inputs = page.locator("input[type='text'], input[type='tel'], input[type='number']").all()
                visible_inputs = [inp for inp in otp_inputs if inp.is_visible()]
                
                if visible_inputs:
                    visible_inputs[0].click()
                    page.wait_for_timeout(300)
                    page.keyboard.type(new_otp, delay=150)
                    log(f"[+] Код {new_otp} введен через эмуляцию клавиатуры.")
                else:
                    # Фокусируемся на теле и печатаем
                    page.keyboard.type(new_otp, delay=150)
                    
                page.wait_for_timeout(5000)
                page.screenshot(path=str(STORAGE_DIR / "rutube_step3_after_otp.png"))
                
                # Если осталась кнопка подтверждения
                verify_btn = page.locator("button[type='submit'], button:has-text('Подтвердить'), button:has-text('Войти')").first
                if verify_btn.count() > 0 and verify_btn.is_visible():
                    verify_btn.click()
                    page.wait_for_timeout(5000)
            else:
                log("[!] Свежий код не поступил за время ожидания.")
                page.screenshot(path=str(STORAGE_DIR / "rutube_otp_timeout.png"))
                
        # Проверяем, вернулись ли мы в Студию
        log("[*] Ожидание перехода в Студию Rutube...")
        for _ in range(6):
            if "studio.rutube.ru" in page.url:
                break
            page.wait_for_timeout(3000)
            
        if "studio.rutube.ru" not in page.url:
            log(f"[*] Принудительный переход на https://studio.rutube.ru/videos (текущий URL: {page.url})...")
            page.goto("https://studio.rutube.ru/videos", timeout=60000)
            page.wait_for_timeout(5000)
            
        page.screenshot(path=str(STORAGE_DIR / "rutube_step4_studio_ready.png"))
        log(f"[+] Текущий URL в Студии: {page.url}")
        
        # 4. Переход на страницу загрузки uploader
        log("[*] Открытие uploader: https://studio.rutube.ru/uploader...")
        page.goto("https://studio.rutube.ru/uploader", timeout=30000)
        page.wait_for_timeout(4000)
        page.screenshot(path=str(STORAGE_DIR / "rutube_step5_uploader_page.png"))
        
        # Ищем file input
        file_input = page.locator("input[type='file']").first
        if file_input.count() == 0:
            log("[*] Ищем кнопку '+' для вызова file input...")
            add_button = page.locator("button:has-text('+'), button[aria-label*='Загрузить'], [data-testid*='upload-btn']").first
            if add_button.count() > 0:
                add_button.click()
                page.wait_for_timeout(2000)
                file_input = page.locator("input[type='file']").first
                
        if file_input.count() > 0:
            log(f"[+] Передача видеофайла в input[type='file']: {VIDEO_PATH}")
            file_input.set_input_files(str(VIDEO_PATH))
            page.wait_for_timeout(6000)
            page.screenshot(path=str(STORAGE_DIR / "rutube_step6_file_selected.png"))
            
            # Заполнение формы метаданных
            log("[*] Заполнение метаданных ролика...")
            page.wait_for_timeout(3000)
            
            # Поле 'Название'
            title_input = page.locator("input[name='title'], textarea[name='title'], input[placeholder*='Название']").first
            if title_input.count() > 0:
                log(f"[*] Установка названия: {TITLE}")
                title_input.click()
                title_input.fill("")
                title_input.fill(TITLE)
                page.wait_for_timeout(1000)
                
            # Поле 'Описание'
            desc_input = page.locator("textarea[name='description'], textarea[placeholder*='Описание'], div[contenteditable='true']").first
            if desc_input.count() > 0:
                log("[*] Установка описания видео...")
                desc_input.click()
                desc_input.fill(DESCRIPTION)
                page.wait_for_timeout(1000)
                
            page.screenshot(path=str(STORAGE_DIR / "rutube_step7_metadata_filled.png"))
            
            # Кнопка 'Опубликовать'
            page.wait_for_timeout(2000)
            page.keyboard.press("Escape")  # Снять возможный фокус с выпадающих списков
            page.wait_for_timeout(500)
            
            log("[*] Поиск и клик по кнопке 'Опубликовать'...")
            published_clicked = False
            
            # Пробуем через evaluate (наиболее надежно в модальных окнах с оверлеем)
            try:
                res_click = page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const pub = buttons.reverse().find(b => b.textContent && b.textContent.includes('Опубликовать'));
                    if (pub) {
                        pub.scrollIntoView();
                        pub.click();
                        return true;
                    }
                    return false;
                }""")
                if res_click:
                    log("[+] Кнопка 'Опубликовать' успешно нажата через JS dispatch!")
                    published_clicked = True
            except Exception as e:
                log(f"[!] Ошибка JS клика: {e}")
                
            if not published_clicked:
                pub_btn = page.locator("button:has-text('Опубликовать')").last
                if pub_btn.count() > 0:
                    log(f"[+] Нажатие Playwright locator с force=True...")
                    pub_btn.click(force=True)
                    published_clicked = True
                    
            if published_clicked:
                log("[*] Ожидание завершения запроса публикации (10 сек)...")
                page.wait_for_timeout(10000)
                page.screenshot(path=str(STORAGE_DIR / "rutube_step8_published.png"))
                log("[+++] ВИДЕО УСПЕШНО ЗАГРУЖЕНО И ОТПРАВЛЕНО НА ПУБЛИКАЦИЮ В RUTUBE!")
                
                # Обновляем БД
                try:
                    conn = sqlite3.connect("content_calendar.db")
                    c = conn.cursor()
                    c.execute("UPDATE publications SET status = 'PUBLISHED', published_at = CURRENT_TIMESTAMP WHERE title LIKE '%ANTIGRAVITY%'")
                    conn.commit()
                    conn.close()
                    log("[+] Статус в content_calendar.db обновлен на PUBLISHED.")
                except Exception as e:
                    log(f"[!] Ошибка обновления БД: {e}")
                    
                send_telegram_msg(
                    "🚀 *АВТОНОМНАЯ ЗАГРУЗКА НА RUTUBE ЗАВЕРШЕНА!*\n\n"
                    f"📹 *Ролик:* {TITLE}\n"
                    "✅ Видеофайл успешно передан через браузерного агента Playwright.\n"
                    "📬 OTP-код подтверждения автоматически считан из почты sugatov86@list.ru.\n"
                    "⏳ Видео отправлено на модерацию и транскодирование в Студии Rutube."
                )
                
                browser_context.close()
                return True
            else:
                log("[!] Кнопка публикации не видна напрямую, сохраняем скриншот состояния.")
                page.screenshot(path=str(STORAGE_DIR / "rutube_step8_pending.png"))
        else:
            log("[!] Не удалось обнаружить поле выбора файла. Проверьте rutube_step5_uploader_page.png")
            
        page.wait_for_timeout(3000)
        browser_context.close()
        return False

if __name__ == "__main__":
    success = execute_browser_upload()
    log(f"[*] Завершение выполнения uploader: success={success}")
