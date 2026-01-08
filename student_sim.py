from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import time

SPAWNER_URL = "https://rhods-dashboard-redhat-ods-applications.apps.ocp-test.nerc.mghpcc.org/notebookController/spawner"
USER_DATA_DIR = "/home/memalhot/.pw-profile"  # create/use a dedicated dir

def execute_bash(page: Page, command: str, delay_ms: int = 2000) -> None:
    page.keyboard.type(command)
    page.keyboard.press("Enter")
    page.wait_for_timeout(delay_ms)

def main():
    workbench_urls = []

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            slow_mo=100,
        )
        page = context.new_page()

        try:
            page.goto(SPAWNER_URL, wait_until="domcontentloaded")

            # wait for the Access Workbench link
            button = page.locator('a[data-id="return-nb-button"], a:has-text("Access workbench")')
            button.wait_for(state="visible", timeout=30_000)
            
            # make sure it always opens in a new page by using the link
            href = button.get_attribute("href")
            if not href:
                raise RuntimeError("Could not find workbench href")

            # open in a new tab
            new_page = context.new_page()
            new_page.goto(href, wait_until="domcontentloaded")

            # save the opened URL
            final_url = new_page.url
            print(f"Opened new workbench tab: {final_url}")
            workbench_urls.append(final_url)

            terminal = new_page.locator(".jp-Terminal").first
            terminal.click()

            execute_bash(new_page, "echo hello")
            execute_bash(new_page, "ls")
            execute_bash(new_page, "pwd")
            execute_bash(new_page, "emacs")

            # keep the browser open
            new_page.wait_for_timeout(10_000)

        finally:
            context.close()


if __name__ == '__main__':
    main()