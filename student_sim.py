from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import time

link = "https://meera-test-ope-test.apps.ocp-test.nerc.mghpcc.org/notebook/ope-test/meera-test/lab"
USER_DATA_DIR = "/home/memalhot/.pw-profile"  # create/use a dedicated dir

def execute_bash(page: Page, command: str, delay_ms: int = 2000) -> None:
    page.keyboard.type(command)
    page.keyboard.press("Enter")
    page.wait_for_timeout(delay_ms)

def main():
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

            execute_bash(page, "echo hello")
            execute_bash(page, "ls")
            execute_bash(page, "pwd")

            execute_bash(page, "emacs")

            # keep the browser open
            page.wait_for_timeout(10_000)

        finally:
            context.close()


if __name__ == '__main__':
    main()