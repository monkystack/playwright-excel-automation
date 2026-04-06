class ExportPage:
    def __init__(self, page):
        self.page = page

    def go_to_export_task_page(self):
        page = self.page

        page.get_by_text("Operations Center").click()
        page.wait_for_timeout(500)

        page.get_by_text("Warehouse Statistics").click()
        page.wait_for_timeout(500)

        page.get_by_role("link", name="Export task information").click()
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Query").click()
        page.wait_for_timeout(1000)

    def get_download_button(self):
        page = self.page
        return page.locator(
            "div.el-table__fixed-right table tbody tr"
        ).nth(0).locator("button.el-button:has-text('Download')")