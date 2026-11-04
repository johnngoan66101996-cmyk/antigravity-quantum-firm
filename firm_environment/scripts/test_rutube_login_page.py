from playwright.sync_api import sync_playwright
from pathlib import Path

def test_login_flow():
    screenshot_dir = Path("firm_environment/storage")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        )
        page = context.new_page()
        print("Navigating to Rutube login...")
        page.goto("https://rutube.ru/multipass/login/?referer=https%3A%2F%2Fstudio.rutube.ru%2Fvideos", timeout=30000)
        page.wait_for_timeout(4000)
        print("Current URL:", page.url)
        print("Page Title:", page.title())
        page.screenshot(path=str(screenshot_dir / "rutube_multipass_page.png"))
        
        # Check inputs
        inputs = page.locator("input").all()
        print(f"Found {len(inputs)} inputs:")
        for idx, inp in enumerate(inputs):
            print(f"  Input #{idx}: name={inp.get_attribute('name')}, type={inp.get_attribute('type')}, placeholder={inp.get_attribute('placeholder')}")
            
        browser.close()

if __name__ == "__main__":
    test_login_flow()
