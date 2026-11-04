import time
import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# Import mail_otp_reader
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPTS_DIR))
import mail_otp_reader

VIDEO_PATH = Path(r"C:\Users\sugat\OneDrive\Desktop\antigravity_v25_promo.mp4")
SCREENSHOTS_DIR = Path("firm_environment/storage")

def wait_for_otp_code(timeout_seconds=60):
    print("[*] Ожидание OTP-кода из почты sugatov86@list.ru...")
    start_time = time.time()
    last_seen_code = None
    
    # Check baseline code first
    initial = mail_otp_reader.get_latest_code()
    if initial.get("status") == "FOUND":
        last_seen_code = initial.get("code")
        print(f"[*] Базовый (прошлый) код: {last_seen_code}")

    while time.time() - start_time < timeout_seconds:
        time.sleep(3)
        res = mail_otp_reader.get_latest_code()
        if res.get("status") == "FOUND":
            code = res.get("code")
            # If it's a fresh code or we see gid.ru
            if code and code != last_seen_code:
                print(f"[+] ПЕРЕХВАЧЕН СВЕЖИЙ КОД ИЗ ПОЧТЫ: {code} (Тема: {res.get('subject')})")
                return code
            elif code and "gid.ru" in res.get("sender", "").lower():
                print(f"[+] Найден код от gid.ru: {code}")
                return code
    print("[-] Таймаут ожидания кода")
    return None

def run_upload_pipeline():
    print("==================================================")
    print("  БРАУЗЕРНЫЙ АГЕНТ: АВТОНОМНАЯ ЗАГРУЗКА RUTUBE    ")
    print("==================================================")
    
    with sync_playwright() as p:
        # Launching real Edge browser
        print("[*] Запуск браузера Edge...")
        browser = p.chromium.launch(
            channel="msedge",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        context = browser.new_context(
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        )
        page = context.new_page()
        
        # 1. Open Rutube Login
        login_url = "https://rutube.ru/multipass/login/?referer=https%3A%2F%2Fstudio.rutube.ru%2Fvideos"
        print(f"[*] Переход на {login_url}...")
        page.goto(login_url, timeout=45000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(SCREENSHOTS_DIR / "upload_step1_login.png"))
        
        # 2. Fill Email
        username_input = page.locator("input[name='username']").first
        if username_input.count() > 0:
            print("[*] Ввод логина sugatov86@list.ru...")
            username_input.click()
            username_input.fill("sugatov86@list.ru")
            page.wait_for_timeout(1000)
            
            submit_btn = page.locator("button[type='submit']").first
            if submit_btn.count() > 0:
                print("[*] Отправка формы логина...")
                submit_btn.click()
                page.wait_for_timeout(4000)
                page.screenshot(path=str(SCREENSHOTS_DIR / "upload_step2_after_email.png"))
                print("[+] Текущий URL:", page.url)
            else:
                print("[-] Кнопка submit не найдена")
        else:
            print("[-] Поле username не найдено, возможно уже авторизованы")
            
        # 3. Check for OTP / Password inputs
        page.wait_for_timeout(2000)
        otp_inputs = page.locator("input[type='text'], input[type='number'], input[type='tel']").all()
        print(f"[*] Найдено полей ввода на шаге 2: {len(otp_inputs)}")
        
        # Check if code requested
        body_text = page.inner_text("body")
        print("--- Фрагмент страницы ---")
        print(body_text[:400])
        print("-------------------------")
        
        if "код" in body_text.lower() or "письмо" in body_text.lower() or "отправили" in body_text.lower():
            code = wait_for_otp_code(timeout_seconds=45)
            if code:
                print(f"[*] Ввод кода {code} в форму...")
                # Try filling code into inputs
                code_digits = list(code)
                digit_inputs = page.locator("input[data-testid*='code'], input[name*='code'], input[autocomplete='one-time-code']").all()
                if not digit_inputs:
                    digit_inputs = [inp for inp in page.locator("input").all() if inp.get_attribute("type") in ["text", "number", "tel"] and inp.is_visible()]
                
                if len(digit_inputs) == len(code_digits):
                    for idx, digit in enumerate(code_digits):
                        digit_inputs[idx].fill(digit)
                        page.wait_for_timeout(200)
                elif len(digit_inputs) > 0:
                    digit_inputs[0].fill(code)
                    
                page.wait_for_timeout(2000)
                # Click submit if present
                sub = page.locator("button[type='submit']").first
                if sub.count() > 0 and sub.is_visible():
                    sub.click()
                page.wait_for_timeout(5000)
                page.screenshot(path=str(SCREENSHOTS_DIR / "upload_step3_after_otp.png"))
                
        # 4. Check if we reached studio.rutube.ru
        print("[*] Переход в Студию Rutube: https://studio.rutube.ru/videos...")
        page.goto("https://studio.rutube.ru/videos", timeout=30000)
        page.wait_for_timeout(5000)
        page.screenshot(path=str(SCREENSHOTS_DIR / "upload_step4_studio.png"))
        print("[+] Текущий URL Студии:", page.url)
        
        # Check if upload button or uploader exists
        add_btn = page.locator("button:has-text('Добавить'), button:has-text('+'), [data-testid*='upload']").first
        print(f"[*] Наличие кнопки Добавить: {add_btn.count() > 0}")
        
        browser.close()

if __name__ == "__main__":
    run_upload_pipeline()
