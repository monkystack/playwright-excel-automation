import time
import os
import psutil
from utils.logging_setup import auto_log


def close_excel_if_open(target_path):
    target_path = os.path.abspath(target_path).lower()

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and "excel" in proc.info['name'].lower():
                for f in proc.open_files():
                    opened = os.path.abspath(f.path).lower()
                    if opened == target_path:
                        print(f"🔒 Excel locking this file: {opened}")
                        print(f"❗ Closing Excel PID: {proc.pid}")
                        proc.terminate()
                        proc.wait(5)
                        return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    return False



@auto_log
def wait_and_download(page, get_button, save_root, retry_interval=90):

    # --- wait for download event ---
    while True:
        btn = get_button()
        print("Trying to click the Download button...")

        try:
            with page.expect_download() as dl:
                btn.click()

            download = dl.value
            print("🎉 Download event detected!")
            break

        except Exception:
            print("⚠️ No download event — task may not be ready.")
            print(f"Retrying after {retry_interval} seconds...")
            time.sleep(retry_interval)

            page.get_by_role("button", name="Query").click()
            page.wait_for_timeout(1000)

    # --- save file manually ---
    os.makedirs(save_root, exist_ok=True)

    ext = os.path.splitext(download.suggested_filename)[1]
    save_path = os.path.join(save_root, "Data" + ext)

    # 🔒 ensure file is not locked by Excel
    close_excel_if_open(save_path)

    # now save
    download.save_as(save_path)
    print("🎉 File saved at:", save_path)

    return save_path