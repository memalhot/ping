from playwright.sync_api import sync_playwright

link = "https://meera-test-ope-test.apps.ocp-test.nerc.mghpcc.org/notebook/ope-test/meera-test/lab"
USER_DATA_DIR = "/home/memalhot/.pw-profile"  # create/use a dedicated dir

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        slow_mo=100,
    )
    page = context.new_page()

    try:
        page.goto(link, wait_until="domcontentloaded")
        page.wait_for_selector("#jp-top-panel", timeout=180_000)

        terminal = page.locator(".jp-Terminal").first
        terminal.click()

        page.keyboard.type("echo hello")
        page.keyboard.press("Enter")

        page.wait_for_timeout(500)

        page.keyboard.type("sleep 2")
        page.keyboard.press("Enter")

        page.wait_for_timeout(3000)

        # keep the browser open
        page.wait_for_timeout(10_000)

    finally:
        context.close()
