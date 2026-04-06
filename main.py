import subprocess
from playwright.sync_api import sync_playwright

from config import DOWNLOAD_DIR, DOWNLOAD_RETRY_INTERVAL
from pages.login_page import LoginPage
from pages.outbound_page import OutboundPage
from pages.export_page import ExportPage
from utils.date_folder import create_today_folder
from utils.download import wait_and_download
import utils.logging_setup
from utils.logging_setup import auto_log, logger

@auto_log

def run():

    today_folder = create_today_folder()

    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=False,
        channel="msedge"
    )
    # Create a browser context and a page
    context = browser.new_context()
    page = context.new_page()

    # Login page (pass BOTH context and page)
    login_page = LoginPage(context, page)
    login_page.login()  # handles timeout and new page automatically

    # Outbound workflow
    outbound = OutboundPage(login_page.page)
    outbound.go_to_outbound_order()
    outbound.query_last_month()
    outbound.export_data()

    # Export task page & download
    export_page = ExportPage(login_page.page)
    export_page.go_to_export_task_page()

    save_path = wait_and_download(
        login_page.page,
        export_page.get_download_button,
        save_root=DOWNLOAD_DIR,
        retry_interval=DOWNLOAD_RETRY_INTERVAL
    )

    print("Final file saved at:", save_path)

    try:
        browser.close()
    finally:
        p.stop()

    # Execute PowerShell script after finishing
    result = subprocess.run([
                            "powershell",
                            "-ExecutionPolicy", "Bypass",
                            "-File", "./scripts/open_vba.ps1",
                            "-OutputFolder", today_folder
                            ])

    if result.returncode != 0:
        logger.error("PowerShell FAILED")
    else:
        logger.info("PowerShell SUCCESS")

if __name__ == "__main__":
    run()