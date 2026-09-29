import re
from pathlib import Path

from playwright.sync_api import Page

from utils.waits_util import WaitUtils
from utils.logger import get_logger


class MaterialCoveragePage:

    def __init__(self, page: Page):

        self.page = page
        self.logger = get_logger("MaterialCoverage")

        # ==================================================
        # Navigation
        # ==================================================

        self.procurement_menu = page.locator(
            "//img[@data-tooltip-id='Procurement']"
        )

        self.material_coverage_link = page.locator(
            "//div[normalize-space()='Material Coverage For Open Sales']"
        )

        # ==================================================
        # Coverage
        # ==================================================

        self.current_coverage = page.get_by_role(
            "button",
            name="Current Coverage"
        )

        self.future_coverage = page.get_by_role(
            "button",
            name="Future Coverage"
        )

        # ==================================================
        # Menu Arrow
        # ==================================================

        self.menu_arrow = page.locator(
            "img[alt='menu']"
        )

        # ==================================================
        # Show All Orders
        # ==================================================

        self.showallorders = page.get_by_role(
            "button",
            name="Show All Orders"
        )

        # ==================================================
        # AG Grid Total Rows
        # ==================================================

        self.total_orders = page.locator(
            "//span[@data-ref='eLabel' and "
            "normalize-space()='Total Rows']"
            "/following-sibling::span[@data-ref='eValue']"
        )

        # ==================================================
        # Excel Export
        # ==================================================

        self.excel_export = page.get_by_text(
            "Excel Export",
            exact=True
        )

        self.download_excel = page.get_by_role(
            "button",
            name="Yes"
        )

        # ==================================================
        # Page Size
        # ==================================================

        self.page_size_input = page.get_by_role(
            "spinbutton",
            name="Custom page size"
        )

        self.page_size_apply_button = (
            self.page_size_input.locator(
                "xpath=following-sibling::button[1]"
            )
        )

        # ==================================================
        # Pagination
        # ==================================================

        self.pagination = page.locator(
            "[data-testid='vf_pagination']"
        )

        self.next_page_button = page.locator(
            "img[alt='Go to next page']"
        )

        self.previous_page_button = page.locator(
            "img[alt='Go to previous page']"
        )

        self.first_page_button = page.locator(
            "img[alt='Go to first page']"
        )

        self.last_page_button = page.locator(
            "img[alt='Go to last page']"
        )

        # ==================================================
        # Grid
        # ==================================================

        self.grid_rows = page.locator(
            "[role='row'][aria-rowindex]"
        )

        self.column_headers = page.get_by_role(
            "columnheader"
        )

        # ==================================================
        # Save
        # ==================================================

        self.save_button = page.get_by_text(
            "Save",
            exact=True
        )

        # ==================================================
        # Toast
        # ==================================================

        self.toast = page.get_by_role(
            "alert"
        )

    # ======================================================
    # Navigation
    # ======================================================

    def open_material_coverage(self):

        self.logger.info(
            "Opening Material Coverage For Open Sales"
        )

        WaitUtils.wait_for_visible(
            self.procurement_menu
        )

        self.procurement_menu.hover()

        WaitUtils.wait_for_visible(
            self.material_coverage_link
        )

        self.material_coverage_link.click()

        WaitUtils.wait_for_visible(
            self.current_coverage
        )

        self.logger.info(
            "Material Coverage page opened successfully"
        )

    # ======================================================
    # Wait for Orders
    # ======================================================

    def wait_for_orders_to_load(self, timeout=60000):

        WaitUtils.wait_for_visible(
            self.total_orders,
            timeout=timeout
        )

        self.page.wait_for_function(
            """
            () => {
                const element = document.querySelector(
                    "[data-ref='eValue']"
                );

                return element &&
                       element.innerText.trim() !== "" &&
                       element.innerText.trim() !== "0";
            }
            """,
            timeout=timeout
        )

    # ======================================================
    # Current Coverage
    # ======================================================

    def click_current_coverage(self):

        WaitUtils.wait_for_visible(
            self.current_coverage
        )

        self.current_coverage.click()

        WaitUtils.wait_for_visible(
            self.current_coverage
        )

    # ======================================================
    # Future Coverage
    # ======================================================

    def click_future_coverage(self):

        WaitUtils.wait_for_visible(
            self.future_coverage
        )

        self.future_coverage.click()

        WaitUtils.wait_for_visible(
            self.future_coverage
        )

    # ======================================================
    # Menu Arrow
    # ======================================================

    def click_menu_arrow(self):

        WaitUtils.wait_for_visible(
            self.menu_arrow
        )

        self.menu_arrow.click()

    # ======================================================
    # Show All Orders
    # ======================================================

    def click_show_all_orders(self):

        WaitUtils.wait_for_visible(
            self.showallorders
        )

        WaitUtils.wait_for_enabled(
            self.showallorders
        )

        self.showallorders.click()

        self.wait_for_orders_to_load()

    # ======================================================
    # Current AG Grid Total Rows
    # ======================================================

    def get_total_orders(self):

        self.wait_for_orders_to_load()

        return (
            self.total_orders
            .inner_text()
            .strip()
            .replace(",", "")
        )

    # ======================================================
    # Page Size
    # ======================================================

    def set_page_size(self, page_size):

        self.logger.info(
            f"Changing page size to {page_size}"
        )

        WaitUtils.wait_for_visible(
            self.page_size_input
        )

        self.page_size_input.fill(
            str(page_size)
        )

        WaitUtils.wait_for_enabled(
            self.page_size_apply_button
        )

        self.page_size_apply_button.click()

        WaitUtils.wait_for_visible(
            self.pagination
        )

        self.wait_for_orders_to_load()

        self.logger.info(
            f"Page size {page_size} applied successfully"
        )

    # ======================================================
    # Current Page Number
    # ======================================================

    def get_current_page_number(self):

        pagination_text = self.pagination.inner_text()

        match = re.search(
            r"Page\s+(\d+)\s+of\s+(\d+)",
            pagination_text,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

        body_text = self.page.locator(
            "body"
        ).inner_text()

        match = re.search(
            r"Page\s+(\d+)\s+of\s+(\d+)",
            body_text,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

        return None

    # ======================================================
    # Next Page
        # ======================================================
    def click_next_page(self):

        WaitUtils.wait_for_visible(
            self.next_page_button
        )

        old_page = self.get_current_page_number()

        self.logger.info(
            f"Clicking Next Page. Current page: {old_page}"
        )

        # Click Next Page
        self.next_page_button.click(
            force=True
        )

        # Give pagination/grid time to react
        self.page.wait_for_timeout(1000)

        # Wait for grid data to load
        self.wait_for_orders_to_load()

        new_page = self.get_current_page_number()

        self.logger.info(
            f"Next Page navigation completed. "
            f"Current page: {new_page}"
        )
    
    # ======================================================
    # First Page
    # ======================================================

    def click_first_page(self):

        WaitUtils.wait_for_visible(
            self.first_page_button
        )

        self.first_page_button.click()

        self.wait_for_orders_to_load()

    # ======================================================
    # Last Page
    # ======================================================

    def click_last_page(self):

        WaitUtils.wait_for_visible(
            self.last_page_button
        )

        self.last_page_button.click()

        self.wait_for_orders_to_load()

    # ======================================================
    # Capture Screenshot
    # ======================================================

    def capture_page_screenshot(self, name):

        screenshot_dir = Path(
            "artifacts",
            "screenshots"
        )

        screenshot_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        screenshot_path = (
            screenshot_dir / f"{name}.png"
        )

        self.page.screenshot(
            path=str(screenshot_path),
            full_page=True
        )

        return screenshot_path

    # ======================================================
    # Capture Current Page Records
    # ======================================================

    def get_current_page_records(self):

        records = []

        rows = self.grid_rows

        for i in range(rows.count()):

            row = rows.nth(i)

            cells = row.get_by_role(
                "gridcell"
            )

            values = []

            for j in range(cells.count()):

                value = (
                    cells.nth(j)
                    .inner_text()
                    .strip()
                )

                values.append(value)

            if values:
                records.append(values)

        return records

    # ======================================================
    # Current Page Row Count
    # ======================================================

    def get_current_page_row_count(self):

        self.wait_for_orders_to_load()

        row_count = self.grid_rows.count()

        self.logger.info(
            f"Current page row count: {row_count}"
        )

        return row_count

    # ======================================================
    # Column Names
    # ======================================================

    def get_column_names(self):

        names = []

        headers = self.column_headers

        for i in range(headers.count()):

            name = (
                headers.nth(i)
                .inner_text()
                .strip()
            )

            if name:
                names.append(name)

        return names

    # ======================================================
    # Swap Columns
    # ======================================================

    def swap_columns(
        self,
        first_column,
        second_column
    ):

        first_header = self.page.locator(
            "[role='columnheader']"
        ).filter(
            has_text=first_column
        ).first

        second_header = self.page.locator(
            "[role='columnheader']"
        ).filter(
            has_text=second_column
        ).first

        WaitUtils.wait_for_visible(
            first_header
        )

        WaitUtils.wait_for_visible(
            second_header
        )

        first_label = first_header.locator(
            ".ag-header-cell-text"
        )

        second_label = second_header.locator(
            ".ag-header-cell-text"
        )

        WaitUtils.wait_for_visible(
            first_label
        )

        WaitUtils.wait_for_visible(
            second_label
        )

        first_box = first_label.bounding_box()
        second_box = second_label.bounding_box()

        if not first_box:
            raise AssertionError(
                f"Could not get position of "
                f"{first_column}"
            )

        if not second_box:
            raise AssertionError(
                f"Could not get position of "
                f"{second_column}"
            )

        first_x = (
            first_box["x"]
            + first_box["width"] / 2
        )

        first_y = (
            first_box["y"]
            + first_box["height"] / 2
        )

        second_x = (
            second_box["x"]
            + second_box["width"] / 2
        )

        second_y = (
            second_box["y"]
            + second_box["height"] / 2
        )

        self.logger.info(
            f"Dragging '{first_column}' "
            f"from ({first_x}, {first_y}) "
            f"to '{second_column}' "
            f"({second_x}, {second_y})"
        )

        self.page.mouse.move(
            first_x,
            first_y
        )

        self.page.mouse.down()

        self.page.mouse.move(
            second_x,
            second_y,
            steps=20
        )

        self.page.mouse.up()

        self.page.wait_for_timeout(1000)

        self.logger.info(
            "Column swap operation completed"
        )

    # ======================================================
    # Save
    # ======================================================

    def click_save(self):

        WaitUtils.wait_for_visible(
            self.save_button
        )

        self.save_button.click()

    # ======================================================
    # Toast
    # ======================================================

    def get_toast_message(self):

        WaitUtils.wait_for_visible(
            self.toast
        )

        return self.toast.inner_text().strip()

    # ======================================================
    # Excel Export
    # ======================================================

    def export_excel(self):

        with self.page.expect_download() as download_info:

            self.excel_export.click()

            self.download_excel.click()

            download = download_info.value
            
            download_dir = (
                        Path(__file__).resolve().parents[1]
                        / "artifacts"
                        / "downloads"
                    )
            
            download_dir.mkdir(
                        parents=True,
                        exist_ok=True
                    )
            
            file_path = (
                        download_dir
                        / download.suggested_filename
                    )
            
            download.save_as(
                        file_path
                    )
            
               
            return file_path
    

    def expand_first_order(self):
        """
        Expand the first order row using the expand/collapse button
        in the pinned-left AG Grid section.
        """
        self.logger.info("Looking for first row expand button")

        expand_button = self.page.locator(
            ".ag-pinned-left-cols-container "
            ".ag-row[row-index='0'] "
            "button"
        ).first

        WaitUtils.wait_for_visible(
            expand_button,
            timeout=30000
        )

        self.logger.info("Clicking first row expand button")

        expand_button.click(force=True)

        self.page.wait_for_timeout(1500)

        self.logger.info("First order expanded successfully")

# ======================================================
    # Main Grid - All Column Names
    # ======================================================

    def get_all_grid_columns(self):
        """
        Collect all main-grid column headers by horizontally
        scrolling through the AG Grid.

        This captures columns that are outside the current viewport.
        """

        self.logger.info("Collecting all main grid columns")

        header_locator = self.page.locator(
            ".ag-header-cell:visible .ag-header-cell-label"
        )

        horizontal_viewport = self.page.locator(
            ".ag-center-cols-viewport"
        ).first

        columns = []

        if horizontal_viewport.count() == 0:
            self.logger.warning(
                "Main grid horizontal viewport was not found"
            )

            for i in range(header_locator.count()):
                text = header_locator.nth(i).inner_text().strip()

                if text and text not in columns:
                    columns.append(text)

            return columns

        horizontal_viewport.evaluate(
            "(element) => element.scrollLeft = 0"
        )

        self.page.wait_for_timeout(500)

        for _ in range(20):

            for i in range(header_locator.count()):
                text = header_locator.nth(i).inner_text().strip()

                if text and text not in columns:
                    columns.append(text)

            scroll_info = horizontal_viewport.evaluate(
                """
                element => ({
                    scrollLeft: element.scrollLeft,
                    clientWidth: element.clientWidth,
                    scrollWidth: element.scrollWidth
                })
                """
            )

            current_position = scroll_info["scrollLeft"]
            client_width = scroll_info["clientWidth"]
            scroll_width = scroll_info["scrollWidth"]

            if current_position + client_width >= scroll_width - 5:
                break

            horizontal_viewport.evaluate(
                """
                element => {
                    element.scrollLeft += element.clientWidth;
                }
                """
            )

            self.page.wait_for_timeout(500)

        horizontal_viewport.evaluate(
            "(element) => element.scrollLeft = 0"
        )

        self.page.wait_for_timeout(300)

        self.logger.info(
            f"Collected {len(columns)} main grid columns"
        )

        return columns

    def print_all_grid_columns(self, title="MAIN GRID COLUMNS"):
        """
        Print all main-grid columns to the execution log.
        """

        columns = self.get_all_grid_columns()

        self.logger.info("=" * 70)
        self.logger.info(title)
        self.logger.info("=" * 70)

        for index, column in enumerate(columns, start=1):
            self.logger.info(
                f"{index}. {column}"
            )

        self.logger.info(
            f"Total Main Grid Columns: {len(columns)}"
        )

        self.logger.info("=" * 70)

        return columns

# ======================================================
    # Expanded Raw Material Grid
    # ======================================================

    def get_expanded_grid_columns(self):
        """
        Collect all columns from the expanded
        Raw Material Details grid.

        The expanded grid is handled separately from the
        main Material Coverage grid.
        """

        self.logger.info(
            "Collecting expanded Raw Material Details columns"
        )

        raw_material_text = self.page.get_by_text(
            "Raw Material Details",
            exact=True
        )

        WaitUtils.wait_for_visible(
            raw_material_text,
            timeout=30000
        )

        # Raw Material Details is followed by the expanded AG Grid.
        expanded_grid = raw_material_text.locator(
            "xpath=following::div[contains(@class,'ag-root-wrapper')][1]"
        )

        WaitUtils.wait_for_visible(
            expanded_grid,
            timeout=30000
        )

        header_locator = expanded_grid.locator(
            ".ag-header-cell:visible .ag-header-cell-label"
        )

        columns = []

        horizontal_viewport = expanded_grid.locator(
            ".ag-center-cols-viewport"
        ).first

        if horizontal_viewport.count() == 0:
            self.logger.warning(
                "Expanded grid horizontal viewport was not found"
            )

            for i in range(header_locator.count()):
                text = header_locator.nth(i).inner_text().strip()

                if text and text not in columns:
                    columns.append(text)

            return columns

        # Start from the left
        horizontal_viewport.evaluate(
            "(element) => element.scrollLeft = 0"
        )

        self.page.wait_for_timeout(500)

        # Scroll through the complete expanded grid
        for _ in range(20):

            for i in range(header_locator.count()):
                text = header_locator.nth(i).inner_text().strip()

                if text and text not in columns:
                    columns.append(text)

            scroll_info = horizontal_viewport.evaluate(
                """
                element => ({
                    scrollLeft: element.scrollLeft,
                    clientWidth: element.clientWidth,
                    scrollWidth: element.scrollWidth
                })
                """
            )

            current_position = scroll_info["scrollLeft"]
            client_width = scroll_info["clientWidth"]
            scroll_width = scroll_info["scrollWidth"]

            if current_position + client_width >= scroll_width - 5:
                break

            horizontal_viewport.evaluate(
                """
                element => {
                    element.scrollLeft += element.clientWidth;
                }
                """
            )

            self.page.wait_for_timeout(500)

        # Return expanded grid to the left
        horizontal_viewport.evaluate(
            "(element) => element.scrollLeft = 0"
        )

        self.page.wait_for_timeout(300)

        self.logger.info(
            f"Collected {len(columns)} expanded grid columns"
        )

        return columns

    def print_expanded_grid_columns(self):
        """
        Print only the Raw Material Details columns.
        """

        columns = self.get_expanded_grid_columns()

        self.logger.info("=" * 70)
        self.logger.info(
            "EXPANDED GRID COLUMNS - RAW MATERIAL DETAILS"
        )
        self.logger.info("=" * 70)

        for index, column in enumerate(columns, start=1):
            self.logger.info(
                f"{index}. {column}"
            )

        self.logger.info(
            f"Total Expanded Grid Columns: {len(columns)}"
        )

        self.logger.info("=" * 70)

        return columns
