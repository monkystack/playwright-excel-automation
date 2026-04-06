from config import url, username, password
from utils.close_popups import close_all_popups
from playwright.sync_api import TimeoutError

class LoginPage:
    def __init__(self, context, page):
        self.context = context  # Browser context, used to create new pages
        self.page = page        # Current active page

    def login(self):
        page = self.page

        try:
            # Try to open the login page, wait up to 60 seconds
            page.goto(url, timeout=60000)
            page.wait_for_load_state("domcontentloaded", timeout=60000)
        except TimeoutError:
            print("Page load timed out. Opening a new page and retrying...")

            # Create a new page
            new_page = self.context.new_page()
            new_page.goto(url, timeout=60000)
            new_page.wait_for_load_state("networkidle", timeout=60000)

            # Close the old page
            try:
                page.close()
                print("Old page closed successfully.")
            except Exception as e:
                print(f"Failed to close old page: {e}")

            # Update self.page to the new page
            page = self.page = new_page

        # Fill in login credentials
        page.get_by_placeholder("User Name / Mobile Number").fill(username)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Sign In").click()

        # Wait for the page to fully load
        page.wait_for_load_state("networkidle", timeout=60000)
        page.reload()
        page.wait_for_load_state("networkidle", timeout=60000)

        # Close any popups after login
        close_all_popups(page)