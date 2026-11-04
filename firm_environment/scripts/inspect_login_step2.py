from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page()
        page.goto("https://rutube.ru/multipass/login/?referer=https%3A%2F%2Fstudio.rutube.ru%2Fvideos")
        page.wait_for_timeout(2000)
        
        page.locator("input[name='username']").fill("sugatov86@list.ru")
        page.locator("button[type='submit']").click()
        page.wait_for_timeout(4000)
        
        print("Page URL:", page.url)
        print("--- Text on Page ---")
        print(page.inner_text("body")[:600])
        print("--------------------")
        
        inputs = page.locator("input").all()
        print(f"Inputs found: {len(inputs)}")
        for i, inp in enumerate(inputs):
            print(f"  #{i}: name={inp.get_attribute('name')}, type={inp.get_attribute('type')}, placeholder={inp.get_attribute('placeholder')}")
            
        browser.close()

if __name__ == "__main__":
    inspect()
