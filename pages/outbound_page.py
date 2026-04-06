class OutboundPage:
    def __init__(self, page):
        self.page = page

    def go_to_outbound_order(self):
        page = self.page

        page.get_by_text("Warehouse Management").click()
        page.wait_for_timeout(1000)

        page.get_by_text("Outbound Mangement").click()
        page.wait_for_timeout(1000)

        page.get_by_role("link", name="Outbound Order").click()
        page.wait_for_timeout(1000)

    def query_last_month(self):
        page = self.page

        page.locator("//label[contains(text(),'Create Time')]/following::input[1]").click()
        page.get_by_text("Last Month").click()
        page.wait_for_timeout(1000)

        page.get_by_role("button", name="Query").click()
        page.wait_for_timeout(1000)

    def export_data(self):
        page = self.page

        page.get_by_role("button", name="Export").click()
        print("🎉 Export button clicked — browser will remain open.")

        page.get_by_role("button", name="Determine").click()
        page.wait_for_timeout(1000)