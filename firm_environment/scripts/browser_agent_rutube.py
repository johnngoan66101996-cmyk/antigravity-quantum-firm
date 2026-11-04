import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path("firm_environment/storage")

def run_browser_login():
    with sync_playwright() as p:
        # Launching Edge with persistent or normal context
        print("[*] Launching browser agent...")
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        )
        page = context.new_page()
        
        url = "https://rutube.ru/multipass/login/?referer=https%3A%2F%2Fstudio.rutube.ru%2Fvideos"
        print(f"[*] Navigating to {url}...")
        page.goto(url, timeout=30000)
        page.wait_for_timeout(3000)
        
        # Take initial screenshot
        page.screenshot(path=str(SCREENSHOTS_DIR / "browser_step1_login.png"))
        print("[+] Step 1 screenshot saved.")
        
        # Look for username input
        username_input = page.locator("input[name='username']").first
        if username_input.count() > 0:
            print("[*] Found username input. Typing sugatov86@list.ru...")
            username_input.click()
            username_input.fill("sugatov86@list.ru")
            page.wait_for_timeout(1000)
            
            # Click continue button
            # Button might be type=submit or button with text
            submit_btn = page.locator("button[type='submit']").first
            if submit_btn.count() > 0:
                print("[*] Clicking submit button...")
                submit_btn.click()
                page.wait_for_timeout(5000)
                page.screenshot(path=str(SCREENSHOTS_DIR / "browser_step2_after_submit.png"))
                print(f"[+] Step 2 URL: {page.url}")
                print("[+] Step 2 screenshot saved.")
            else:
                print("[-] Submit button not found")
        else:
            print("[-] Username input not found")
            
        browser.close()

if __name__ == "__main__":
    run_browser_login()
