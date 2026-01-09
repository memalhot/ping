from playwright.sync_api import sync_playwright, Page, TimeoutError as PWTimeoutError
import threading
import time


USER_DATA_DIR = "/home/memalhot/.pw-profile"  # create/use a dedicated dir
workbench_urls = []


# assume 10 nbs based on launch scripts
urls = [f"https://notebook-{i}-mm-pingtest.apps.ocp-test.nerc.mghpcc.org/notebook/mm-pingtest/notebook-{i}/lab?" for i in range(1, 11)]


def bootstrap_login_and_save_state(login_url: str, state_path: str = "auth.json"):
   from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
   with sync_playwright() as p:
       browser = p.chromium.launch(headless=False)
       context = browser.new_context()
       page = context.new_page()


       page.goto(login_url, wait_until="domcontentloaded")
       page.wait_for_url("**/lab**", timeout=120_000)
       try:
           page.wait_for_load_state("networkidle", timeout=10_000)
       except PWTimeoutError:
           pass


       context.storage_state(path=state_path)
       browser.close()




def ensure_authed_via_github(page: Page) -> None:
   """
   If on the RHODS/JupyterHub oauth login page, click the 'github' button.
   Then wait until back on the notebook /lab page.
   """
   github_button = page.locator("a[title='Log in with github']")
   try:
       github_button.wait_for(state="visible", timeout=3_000)


       with page.expect_navigation(wait_until="domcontentloaded", timeout=30_000):
               github_button.click()
               page.wait_for_url("**/lab**", timeout=120_000)
   except PWTimeoutError:
       return


def execute_bash(page: Page, command: str, delay_ms: int = 2000) -> None:
   page.keyboard.type(command)
   page.keyboard.press("Enter")
   page.wait_for_timeout(delay_ms)


def open_terminal(page: Page) -> None:
   page.get_by_role("menuitem", name="File").click()
   page.wait_for_selector("ul.lm-Menu-content[role='menu']", timeout=10_000)
   page.locator("ul.lm-Menu-content .lm-Menu-itemLabel", has_text="New").hover()
   page.wait_for_function(
       "() => document.querySelectorAll('ul.lm-Menu-content[role=\"menu\"]').length >= 2",
       timeout=10_000,
   )
   menus = page.locator("ul.lm-Menu-content[role='menu']")
   submenu = menus.nth(menus.count() - 1)
   submenu.locator(".lm-Menu-itemLabel", has_text="Terminal").click()
   page.wait_for_selector(".xterm-screen", timeout=30_000)
   page.locator(".xterm-screen").click()


def run_notebook(url, state_path: str = "auth.json"):
   with sync_playwright() as p:
       browser = p.chromium.launch(headless=False)
       context = browser.new_context(storage_state=state_path)


       page = context.new_page()
       page.goto(url, wait_until="domcontentloaded")
       page.wait_for_timeout(5_000)


       ensure_authed_via_github(page)
       page.wait_for_timeout(2_000)


       open_terminal(page)


       execute_bash(page, "echo 'Terminal is working'")
       execute_bash(page, "pwd")
       page.wait_for_timeout(30_000)


       context.close()


def main():
   bootstrap_login_and_save_state(
       login_url="https://notebook-1-mm-pingtest.apps.ocp-test.nerc.mghpcc.org/notebook/mm-pingtest/notebook-1/lab?"
   )


   threads = []
   for url in urls:
       t = threading.Thread(target=run_notebook, args=(url,))
       t.start()
       time.sleep(2)
       threads.append(t)


   for t in threads:
       t.join()


if __name__ == "__main__":
   main()
