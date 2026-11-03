"""
Скрипт загрузки видео на Rutube через Playwright с использованием cookies сессии
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
VIDEO_PATH = STORAGE_DIR / "antigravity_v25_promo.mp4"

def upload():
    cookie_dict = json.load(open(STORAGE_DIR / "rutube_session.json", "r", encoding="utf-8"))
    cookies = []
    for k, v in cookie_dict.items():
        cookies.append({
            "name": k,
            "value": v,
            "domain": ".rutube.ru",
            "path": "/"
        })

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        
        # Переход на страницу добавления видео
        print("Переход в Студию загрузки Rutube...")
        page.goto("https://studio.rutube.ru/uploader", timeout=30000)
        page.wait_for_timeout(3000)
        print("URL:", page.url)
        
        # Проверяем, есть ли поле загрузки файла (input type=file)
        file_input = page.locator("input[type='file']").first
        if file_input.count() > 0:
            print("Поле загрузки найдено! Передаём видеофайл...")
            file_input.set_input_files(str(VIDEO_PATH))
            page.wait_for_timeout(5000)
            print("Видеофайл передан в форму загрузки!")
            page.screenshot(path=str(STORAGE_DIR / "rutube_upload_progress.png"))
        else:
            print("Поле загрузки не найдено на странице, текущий URL:", page.url)
            page.screenshot(path=str(STORAGE_DIR / "rutube_upload_fail.png"))
            
        browser.close()

if __name__ == "__main__":
    upload()
