import re
from pathlib import Path

from playwright.sync_api import Page

from utils.waits_util import WaitUtils
from utils.logger import get_logger


logger = get_logger("ProcurementPlanningPage")


class ProcurementPlanningPage:

    def __init__(self, page: Page):
        self.page = page

        # ======================================================
        # Procurement Planning Navigation
        # ======================================================

        self.procurement_menu = page.locator(
            "//img[@data-tooltip-id='Procurement']"
        )

        self.procurement_planning_menu = page.locator(
            "//div[normalize-space()='Procurement Planning']"
        )

        # ======================================================
        # Completely Available
        # ======================================================

        self.completely_available_button = page.get_by_role(
            "button",
            name="Completely Available",
            exact=True
        )

        # ======================================================
        # First Row / Expand
        # ======================================================

        self.first_row = page.locator(
            ".ag-pinned-left-cols-container "
            "[role='row'][row-index='0']"
        )

        self.first_row_first_cell = self.first_row.locator(
            "[role='gridcell']"
        ).first

        self.expand_button = self.first_row_first_cell.locator(
            "span.ag-group-contracted "
            "img[src*='expand.svg']"
        ).first

        # ======================================================
        # Excel Export
        # ======================================================

        self.excel_export = page.get_by_text(
            "Excel Export",
            exact=True
        )

        self.excel_dropdown = page.get_by_text(
            "Select...",
            exact=True
        )

        self.excel_ok_button = page.get_by_role(
            "button",
            name="Ok",
            exact=True
        )

        # ======================================================
        # Pagination
        # ======================================================

        self.page_size_input = page.locator(
            "input[aria-label='Custom page size']"
        )

        self.page_size_apply_button = page.locator(
            "input[aria-label='Custom page size'] + button"
        )

        self.next_page_button = page.locator(
            "img[alt='Go to next page']"
        )

        self.first_page_button = page.locator(
            "img[alt='Go to first page']"
        )

        # ======================================================
        # Column Swap
        # ======================================================

        self.rm_description_column = page.locator(
            "[role='columnheader'][col-id='RMDescription']"
        )

        self.color_priority_column = page.locator(
            "[role='columnheader'][col-id='ColorPriority']"
        )

        self.column_headers = page.locator(
            ".ag-header-row-column [role='columnheader']"
        )

        # ======================================================
        # Save Layout
        # ======================================================

        # Locator and method intentionally have different names.
        # This avoids:
        # TypeError: 'Locator' object is not callable
        self.save_layout_button = page.get_by_text(
            "Save Layout",
            exact=True
        )

        # ======================================================
        # Toast
        # ======================================================

        # Used to wait until a toast is no longer blocking
        # the Save Layout button.
        self.toast_message = page.locator(
            "[role='alert']"
        )
       
        
        self.reset_layout_button = page.get_by_text(
        "Reset Layout",
        exact=True
    )
    # ==========================================================
    # Procurement Planning Navigation
    # ==========================================================

    def click_procurement_menu(self):

        logger.info(
            "Hovering over Procurement menu"
        )

        self.procurement_menu.hover()

        WaitUtils.wait_for_visible(
            self.procurement_planning_menu,
            timeout=60000
        )

        logger.info(
            "Clicking Procurement Planning"
        )

        self.procurement_planning_menu.click()

        logger.info(
            "Procurement Planning opened successfully"
        )

    # ==========================================================
    # Completely Available
    # ==========================================================

    def click_completely_available(self):

        logger.info(
            "Clicking Completely Available"
        )

        WaitUtils.wait_for_visible(
            self.completely_available_button,
            timeout=60000
        )

        WaitUtils.wait_for_enabled(
            self.completely_available_button,
            timeout=60000
        )

        self.completely_available_button.click()

        logger.info(
            "Completely Available opened successfully"
        )

    # ==========================================================
    # Wait For Completely Available Data
    # ==========================================================

    def wait_for_data_load(self):

        logger.info(
            "Waiting for Completely Available data to load"
        )

        self.page.wait_for_function(
            """
            () => {
                const text = document.body.innerText;

                const match = text.match(
                    /(\\d+)\\s+to\\s+(\\d+)\\s+of\\s+(\\d+)/
                );

                if (!match) {
                    return false;
                }

                const total = Number(match[3]);

                return total > 0;
            }
            """,
            timeout=60000
        )

        logger.info(
            "Completely Available data loaded successfully"
        )

    # ==========================================================
    # Expand First Row
    # ==========================================================

    def expand_first_row(self):

        logger.info(
            "Waiting for Completely Available grid data"
        )

        WaitUtils.wait_for_visible(
            self.first_row,
            timeout=60000
        )

        logger.info(
            "Grid first row is available"
        )

        WaitUtils.wait_for_visible(
            self.expand_button,
            timeout=60000
        )

        logger.info(
            "Clicking expand button for first row"
        )

        self.expand_button.click()

        logger.info(
            "First row expanded successfully"
        )

    # ==========================================================
    # Get Total Record Count
    # ==========================================================

    def get_total_record_count(self):

        logger.info(
            "Capturing total record count from pagination"
        )

        # Always wait for actual data before reading pagination.
        self.wait_for_data_load()

        body_text = self.page.locator(
            "body"
        ).inner_text()

        matches = re.findall(
            r"(\d+)\s+to\s+(\d+)\s+of\s+(\d+)",
            body_text
        )

        logger.info(
            f"Pagination values found: {matches}"
        )

        if not matches:
            raise AssertionError(
                "Pagination text was not found "
                "after data loaded"
            )

        # Use the last pagination occurrence.
        start, end, total = matches[-1]

        total_count = int(total)

        logger.info(
            f"Pagination text: "
            f"{start} to {end} of {total}"
        )

        logger.info(
            f"Total record count: {total_count}"
        )

        return total_count

    # ==========================================================
    # Excel Export
    # ==========================================================

    def export_excel(self):

        logger.info(
            "Clicking Excel Export"
        )

        WaitUtils.wait_for_visible(
            self.excel_export,
            timeout=60000
        )

        self.excel_export.click()

        logger.info(
            "Excel Export popup opened"
        )

        WaitUtils.wait_for_visible(
            self.excel_dropdown,
            timeout=60000
        )

        self.excel_dropdown.click()

        completely_available_option = (
            self.page.get_by_text(
                "Completely Available",
                exact=True
            ).last
        )

        WaitUtils.wait_for_visible(
            completely_available_option,
            timeout=60000
        )

        completely_available_option.click()

        logger.info(
            "Completely Available Excel selected"
        )

        WaitUtils.wait_for_visible(
            self.excel_ok_button,
            timeout=60000
        )

        WaitUtils.wait_for_enabled(
            self.excel_ok_button,
            timeout=60000
        )

        logger.info(
            "Clicking OK to download Excel"
        )

        with self.page.expect_download(
            timeout=60000
        ) as download_info:

            self.excel_ok_button.click()

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

        logger.info(
            f"Excel downloaded successfully: "
            f"{file_path}"
        )

        return file_path

    # ==========================================================
    # Set Page Size
    # ==========================================================

    def set_page_size(self, page_size):

        logger.info(
            f"Changing page size to {page_size}"
        )

        WaitUtils.wait_for_visible(
            self.page_size_input,
            timeout=60000
        )

        self.page_size_input.fill(
            str(page_size)
        )

        logger.info(
            f"Page size value entered: {page_size}"
        )

        WaitUtils.wait_for_visible(
            self.page_size_apply_button,
            timeout=60000
        )

        self.page_size_apply_button.click()

        logger.info(
            f"Page size {page_size} applied successfully"
        )

    # ==========================================================
    # Next Page
    # ==========================================================

    def click_next_page(self):

        logger.info(
            "Clicking Next Page"
        )

        WaitUtils.wait_for_visible(
            self.next_page_button,
            timeout=60000
        )

        self.next_page_button.click()

        logger.info(
            "Next Page clicked successfully"
        )

    # ==========================================================
    # First Page
    # ==========================================================

    def go_to_first_page(self):

        logger.info(
            "Checking current pagination state"
        )

        if self.first_page_button.is_visible():

            logger.info(
                "Clicking First Page"
            )

            self.first_page_button.click()

            self.page.wait_for_timeout(1000)

            logger.info(
                "Returned to first page"
            )

    # ==========================================================
    # Get Column Order
    # ==========================================================

    def get_column_order(self):

        logger.info(
            "Capturing current column order"
        )

        columns = self.column_headers.evaluate_all(
            """
            headers => headers
                .map(header => header.getAttribute('col-id'))
                .filter(colId => colId)
            """
        )

        logger.info(
            f"Current column order: {columns}"
        )

        return columns

    # ==========================================================
    
        # ==========================================================
        # Wait For Toast To Disappear
        # ==========================================================

    def wait_for_toast_to_disappear(self):  
            logger.info(
                "Checking for visible toast message"
            )

            # If the toast exists, wait until it is hidden.
            if self.toast_message.count() > 0:

                try:
                    self.toast_message.first.wait_for(
                        state="hidden",
                        timeout=60000
                    )

                except Exception:
                    logger.info(
                        "Toast did not become hidden "
                        "within the expected time"
                    )

            logger.info(
                "Toast is no longer blocking the page"
            )

    # ==========================================================
    # Save Layout
    # ==========================================================

    def save_layout(self):

        logger.info(
            "Waiting for toast message to disappear "
            "before clicking Save Layout"
        )

        self.wait_for_toast_to_disappear()

        logger.info(
            "Clicking Save Layout"
        )

        WaitUtils.wait_for_visible(
            self.save_layout_button,
            timeout=60000
        )

        WaitUtils.wait_for_enabled(
            self.save_layout_button,
            timeout=60000
        )

        self.save_layout_button.click()

        logger.info(
            "Save Layout clicked successfully"
        )
        
        
            
    def swap_rm_description_and_color_priority(self):
        logger.info(
            "Swapping Color Priority and RM Description columns"
        )

        WaitUtils.wait_for_visible(
            self.color_priority_column,
            timeout=60000
        )

        WaitUtils.wait_for_visible(
            self.rm_description_column,
            timeout=60000
        )

        before_columns = self.get_column_order()

        logger.info(
            f"Column order BEFORE swap: {before_columns}"
        )

        logger.info(
            "Dragging ColorPriority to RMDescription"
        )

        self.color_priority_column.drag_to(
            self.rm_description_column,
            timeout=60000
        )

        # Give AG Grid time to complete the drag operation
        self.page.wait_for_timeout(2000)

        after_drag_columns = self.get_column_order()

        logger.info(
            f"Column order AFTER drag: {after_drag_columns}"
        )

        logger.info(
            "Column drag operation completed"
        )
            
    def reset_layout(self):

        logger.info("Resetting grid layout")

        WaitUtils.wait_for_visible(
            self.reset_layout_button,
            timeout=60000
        )

        WaitUtils.wait_for_enabled(
            self.reset_layout_button,
            timeout=60000
        )

        self.reset_layout_button.click()

        self.page.wait_for_timeout(2000)

        logger.info(
            "Reset Layout clicked successfully"
        )