from utils.logging_setup import auto_log

@auto_log
def close_all_popups(page):
    """
    Generic popup closer: automatically clicks any modal/dialog buttons.
    """
    selectors = [
        ".el-button"
    ]

    for _ in range(5):
        popup_found = False

        for selector in selectors:
            try:
                buttons = page.query_selector_all(selector)
                for btn in buttons:
                    text = (btn.inner_text() or "").strip()
                    if text in ["", "×"]:
                        continue

                    try:
                        print(f"Attempting to close popup → Button: {text}")
                        btn.click(timeout=400)
                        popup_found = True
                        page.wait_for_timeout(400)
                    except:
                        pass

            except:
                continue

        if not popup_found:
            print("✔ No more popups detected — all cleared.")
            break