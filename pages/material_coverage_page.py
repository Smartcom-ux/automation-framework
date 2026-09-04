from playwright.sync_api import Page, expect


class MaterialCoveragePage:

    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.menu_logo = page.get_by_role(
            "img",
            name="logo"
        )

        self.material_coverage = page.get_by_text(
            "Material Coverage For Open Sales",
            exact=True
        )

        # Plant
        self.plant_button = page.get_by_role(
            "button",
            name="1014"
        )

        # Export
        self.excel_export = page.get_by_test_id(
            "vf-button-outline"
        )

    def open_material_coverage(self):
        self.menu_logo.click(button="right")

        self.page.get_by_text(
            "Welcome to VectorFlowA"
        ).click()

        self.page.get_by_role(
            "img",
            name="logo",
            description=(
                "Procurement Material Coverage For Open Sales "
                "arrow Procurement Planning arrow "
                "Material Requirement arrow "
                "Day Wise Coverage arrow "
                "RM/PM Orderwise Coverage arrow "
                "RM/PM Buffer Trend arrow "
                "Expediting RM/Suppliers arrow"
            )
        ).click()

        self.material_coverage.click()

    def select_plant(self):
        self.plant_button.click()

    def export_excel(self):
        self.page.get_by_text(
            "Go Back+ Add FilterExcel"
        ).click()

        self.page.locator(
            "div"
        ).filter(
            has_text="Excel Export"
        ).click()

        with self.page.expect_download() as download_info:
            self.excel_export.click()

        return download_info.value