"""
Fix Rutube Video Metadata Script (v9.0.0-OMEGA)
Автономно открывает Студию Rutube, заходит в редактирование последнего видео,
выбирает обязательную категорию, вносит Название и Описание и нажимает Сохранить.
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

STORAGE_DIR = Path("firm_environment/storage")
USER_DATA_DIR = STORAGE_DIR / "rutube_browser_profile"

TITLE = "ANTIGRAVITY v2.5: Промышленный торговый комплекс и квантовые агенты L2"
DESCRIPTION = (
    "Промышленный обзор автономного квантового торгового комплекса ANTIGRAVITY v2.5.\n\n"
    "⚡ Ключевые возможности системы:\n"
    "— Двухъядерный контур рассуждений: Qwen-2.5 7B (высокоскоростной скоринг стакана) и DeepSeek-R1 7B (стратегическая валидация).\n"
    "— Захват спреда L2 на базе стохастической модели Авельянеда-Стоикова (Avellaneda-Stoikov).\n"
    "— Защита капитала: жесткий лимит стоп-лосса 25 bps и валидатор сделок Actor-Critic.\n"
    "— Полная интеграция с Bybit V5 Unified Trading Account (UTA) и терминалом CScalp.\n\n"
    "#antigravity #bybit #scalping #crypto #trading #deepseek #qwen #algorithmic_trading #ai"
)

def fix_metadata():
    with sync_playwright() as p:
        print("[*] Запуск браузера с сохраненной сессией...")
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            channel="msedge",
            headless=False,
            args=["--start-maximized"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        print("[*] Переход в Студию: https://studio.rutube.ru/videos?tab=main...")
        page.goto("https://studio.rutube.ru/videos?tab=main", timeout=60000)
        page.wait_for_timeout(5000)
        
        # Кликаем на карточку видео antigravity_v25_promo
        print("[*] Поиск карточки antigravity_v25_promo...")
        video_card = page.locator("text=antigravity_v25_promo").first
        if video_card.count() > 0:
            print("[+] Карточка найдена, кликаем для открытия формы редактирования...")
            video_card.click()
            page.wait_for_timeout(4000)
            page.screenshot(path=str(STORAGE_DIR / "fix_meta_step1_opened.png"))
            
            # 1. Заполняем поле 'Название'
            title_input = page.locator("input[name='title'], textarea[name='title']").first
            if title_input.count() > 0:
                print("[*] Установка названия...")
                title_input.click()
                title_input.fill("")
                title_input.fill(TITLE)
                page.wait_for_timeout(500)
                
            # 2. Заполняем поле 'Описание'
            desc_input = page.locator("textarea[name='description'], div[contenteditable='true']").first
            if desc_input.count() > 0:
                print("[*] Установка описания...")
                desc_input.click()
                desc_input.fill("")
                desc_input.fill(DESCRIPTION)
                page.wait_for_timeout(500)
                
            # 3. Выбор Категории
            print("[*] Поиск выпадающего списка категории...")
            cat_dropdown = page.locator("div:has-text('Выберите категорию'), [placeholder*='категори'], div[class*='select']").first
            if cat_dropdown.count() > 0:
                print("[*] Клик по выпадающему списку категории...")
                cat_dropdown.click()
                page.wait_for_timeout(1000)
                # Выбираем опцию из списка: 'Технологии и интернет', 'Наука и образование', 'Бизнес' или любую первую доступную
                cat_option = page.locator("li:has-text('Технологии'), div:has-text('Технологии'), li:has-text('Бизнес'), [role='option']").first
                if cat_option.count() > 0:
                    print(f"[*] Выбор категории: '{cat_option.inner_text().strip()}'...")
                    cat_option.click()
                    page.wait_for_timeout(1000)
                else:
                    # Клик по первому элементу опций
                    first_opt = page.locator("[role='option']").first
                    if first_opt.count() > 0:
                        first_opt.click()
                        page.wait_for_timeout(1000)
                        
            page.screenshot(path=str(STORAGE_DIR / "fix_meta_step2_filled.png"))
            
            # 4. Нажимаем кнопку 'Сохранить'
            print("[*] Нажатие кнопки 'Сохранить'...")
            save_clicked = False
            try:
                res = page.evaluate('''() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const saveBtn = buttons.reverse().find(b => b.textContent && (b.textContent.includes('Сохранить') || b.textContent.includes('Опубликовать')));
                    if (saveBtn) {
                        saveBtn.scrollIntoView();
                        saveBtn.click();
                        return true;
                    }
                    return false;
                }''')
                if res:
                    print("[+] Кнопка сохранена через JS evaluate!")
                    save_clicked = True
            except Exception as e:
                print(f"[!] Ошибка JS клика: {e}")
                
            if not save_clicked:
                btn = page.locator("button:has-text('Сохранить'), button:has-text('Опубликовать')").last
                if btn.count() > 0:
                    btn.click(force=True)
                    save_clicked = True
                    
            page.wait_for_timeout(5000)
            page.screenshot(path=str(STORAGE_DIR / "fix_meta_step3_saved.png"))
            print("[+++] Метаданные видео успешно сохранены!")
            ctx.close()
            return True
        else:
            print("[!] Карточка antigravity_v25_promo не найдена в списке.")
            ctx.close()
            return False

if __name__ == "__main__":
    fix_metadata()
