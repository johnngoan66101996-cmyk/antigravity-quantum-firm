"""
Автоматическое сохранение упаковки канала Rutube через Playwright + Edge
"""

import json
from playwright.sync_api import sync_playwright
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"

cookie_dict = json.load(open(STORAGE_DIR / "rutube_session.json", "r", encoding="utf-8"))
cookies = []
for k, v in cookie_dict.items():
    cookies.append({
        "name": k,
        "value": v,
        "domain": ".rutube.ru",
        "path": "/"
    })

CHANNEL_TITLE = "Квантовый ИИ: Claude Code, GPT & Нейросети"
CHANNEL_DESC = (
    "Практическая архитектура автономных ИИ-агентов, связки Claude Code, GPT и GLM, "
    "квантово-когнитивные алгоритмы и автоматизация коммерческих процессов без сторонних платформ.\n\n"
    "Разборы промптов, код локальных систем и живые тесты.\n"
    "Связь и интеграции: @list.ru"
)

def save_channel():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        page.goto("https://studio.rutube.ru/channel-settings/channel", timeout=30000)
        page.wait_for_timeout(3000)
        
        print("Текущий URL:", page.url)
        
        # Находим поле названия канала
        title_input = page.locator("input[name='name'], input[placeholder*='название'], input").first
        if title_input:
            title_input.fill(CHANNEL_TITLE)
            print("Название заполнено:", CHANNEL_TITLE)
            
        # Находим поле описания (textarea)
        desc_area = page.locator("textarea").first
        if desc_area:
            desc_area.fill(CHANNEL_DESC)
            print("Описание заполнено!")
            
        page.wait_for_timeout(1000)
        
        # Находим кнопку Сохранить
        save_btn = page.locator("button:has-text('Сохранить'), button[type='submit']").first
        if save_btn:
            is_enabled = save_btn.is_enabled()
            print("Кнопка Сохранить активна:", is_enabled)
            if is_enabled:
                save_btn.click()
                page.wait_for_timeout(3000)
                print(">>> КНОПКА 'СОХРАНИТЬ' УСПЕШНО НАЖАТА АГЕНТОМ!")
            else:
                print("Кнопка 'Сохранить' неактивна (возможно, изменения уже применились)")
                
        # Скриншот результата
        screenshot_path = STORAGE_DIR / "rutube_saved_result.png"
        page.screenshot(path=str(screenshot_path))
        print("Скриншот сохранён:", screenshot_path)
        browser.close()

if __name__ == "__main__":
    save_channel()
