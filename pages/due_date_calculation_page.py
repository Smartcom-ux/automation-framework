from playwright.sync_api import Page

from utils.waits_util import WaitUtils
from utils.logger import get_logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = get_logger("DueDateCalculationPage")


class DueDateCalculationPage:

    def __init__(self, page: Page):
        self.page = page

        # ---------------------------------------------------------
        # Production Planning & Scheduling
        # ---------------------------------------------------------

        self.production_menu = page.locator(
            "img[data-tooltip-id="
            "'navbar.listMenuParent.prodAndPlanningScheduling.title']"
        )

        self.ddq_menu = page.get_by_text(
            "Due Date Quotation",
            exact=True
        )

        # ---------------------------------------------------------
        # Order Selection
        # ---------------------------------------------------------

        # First data-row checkbox only
        # Excludes AG Grid header Select All checkbox
        self.order_checkbox = page.locator(
            ".ag-pinned-left-cols-container "
            ".ag-row "
            "input.ag-checkbox-input"
        ).first

        # Checkbox on the page after Continue
        self.order_checkbox_after_continue = page.locator(
            "input[type='checkbox'].ag-checkbox-input"
        ).last

        self.continue_button = page.get_by_role(
            "button",
            name="Continue",
            exact=True
        )

        self.edit_button = page.get_by_role(
            "button",
            name="Edit",
            exact=True
        )

        # ---------------------------------------------------------
        # DDQ Dropdowns
        # ---------------------------------------------------------

        self.ddq_dropdowns = page.locator(
            "div[class*='control']"
        )

        # ---------------------------------------------------------
        # DDQ Action Buttons
        # ---------------------------------------------------------

        self.save_button = page.get_by_role(
            "button",
            name="Save",
            exact=True
        )

        self.calculate_due_date_button = page.get_by_role(
            "button",
            name="Calculate Due Date",
            exact=True
        )

        self.confirm_button = page.get_by_role(
            "button",
            name="Confirm",
            exact=True
        )

        self.schedule_button = page.get_by_role(
            "button",
            name="Schedule",
            exact=True
        )
        self.restricted_warning = self.page.get_by_text(
            "Access to this page is restricted because due date assignment is automatic in the current system.",
            exact=True
        )
    # =============================================================
    # Navigation
    # =============================================================

    def due_date_calculation(self):
        logger.info(
            "Navigating to Due Date Quotation"
        )

        WaitUtils.wait_for_visible(
            self.production_menu
        )

        self.production_menu.hover()

        WaitUtils.wait_for_visible(
            self.ddq_menu
        )

        self.ddq_menu.click()

        logger.info(
            "Due Date Quotation page opened successfully"
        )

    # =============================================================
    # Order Selection
    # =============================================================

    def select_order(self):
        logger.info(
            "Selecting first order"
        )

        WaitUtils.wait_for_visible(
            self.order_checkbox
        )

        self.order_checkbox.check()

        logger.info(
            "First order selected successfully"
        )

    def click_continue(self):
        logger.info(
            "Clicking Continue button"
        )

        WaitUtils.wait_for_visible(
            self.continue_button
        )

        self.continue_button.click()

        logger.info(
            "Continue button clicked successfully"
        )

    def select_order_after_continue(self):
        logger.info(
            "Selecting order after Continue"
        )

        WaitUtils.wait_for_visible(
            self.order_checkbox_after_continue
        )

        self.order_checkbox_after_continue.check()

        logger.info(
            "Order selected successfully after Continue"
        )

    def click_edit(self):
        logger.info(
            "Clicking Edit button"
        )

        WaitUtils.wait_for_visible(
            self.edit_button
        )

        self.edit_button.click()

        logger.info(
            "Edit button clicked successfully"
        )

    # =============================================================
    # DDQ Dropdowns
    # =============================================================

    def select_ddq_dropdowns(self, dropdown_index):

        dropdown_number = dropdown_index + 1

        logger.info(
            f"Opening DDQ Dropdown {dropdown_number}"
        )

        dropdown = self.ddq_dropdowns.nth(
            dropdown_index
        )

        WaitUtils.wait_for_visible(
            dropdown
        )

        dropdown.click()

        options = self.page.locator(
            "div[class*='menu'] "
            "div[class*='option']"
        )

        # Check whether the dropdown has any options.
        # DD4 currently has no data and should be skipped.
        option_count = options.count()

        if option_count == 0:

            logger.info(
                f"DDQ Dropdown {dropdown_number} "
                f"has no options. Skipping."
            )

            self.page.keyboard.press("Escape")

            return

        first_option = options.first

        WaitUtils.wait_for_visible(
            first_option
        )

        option_text = first_option.inner_text().strip()

        logger.info(
            f"DDQ Dropdown {dropdown_number} "
            f"selecting first option: {option_text}"
        )

        first_option.click()

        logger.info(
            f"DDQ Dropdown {dropdown_number} "
            f"first option selected successfully"
        )

    # =============================================================
    # Save
    # =============================================================

    def click_save(self):
        logger.info(
            "Clicking Save button"
        )

        WaitUtils.wait_for_visible(
            self.save_button
        )

        WaitUtils.wait_for_enabled(
            self.save_button
        )

        self.save_button.click(
            force=True
        )

        logger.info(
            "Save button clicked successfully"
        )

    # =============================================================
    # Calculate Due Date
    # =============================================================

    def click_calculate_due_date(self):
        logger.info(
            "Waiting for Calculate Due Date button"
        )

        WaitUtils.wait_for_visible(
            self.calculate_due_date_button
        )

        WaitUtils.wait_for_enabled(
            self.calculate_due_date_button
        )

        logger.info(
            "Clicking Calculate Due Date button"
        )

        self.calculate_due_date_button.click()

        logger.info(
            "Calculate Due Date button clicked successfully"
        )

    # =============================================================
    # Confirm
    # =============================================================

    def click_confirm(self):
        logger.info(
            "Clicking Confirm button"
        )

        WaitUtils.wait_for_visible(
            self.confirm_button
        )

        WaitUtils.wait_for_enabled(
            self.confirm_button
        )

        self.confirm_button.click()

        logger.info(
            "Confirm button clicked successfully"
        )

    # =============================================================
    # Schedule
    # =============================================================

    def click_schedule(self):
        logger.info(
            "Clicking Schedule button"
        )

        WaitUtils.wait_for_visible(
            self.schedule_button
        )

        WaitUtils.wait_for_enabled(
            self.schedule_button
        )

        self.schedule_button.click()

        logger.info(
            "Schedule button clicked successfully"
        )

    # =============================================================
    # Schedule Toast
    # =============================================================

    def capture_schedule_toast(self):

        expected_message = (
            "Orders Scheduled Successfully"
        )

        logger.info(
            "Waiting for Schedule success toast"
        )

        toast = self.page.get_by_text(
            expected_message,
            exact=True
        )

        WaitUtils.wait_for_visible(
            toast
        )

        message = toast.first.inner_text().strip()

        logger.info(
            f"Schedule toast captured: {message}"
        )

        assert message == expected_message, (
            f"Expected toast '{expected_message}', "
            f"but received '{message}'"
        )

        logger.info(
            "Schedule success toast validated successfully"
        )

        return message
    
    def check_access_restriction(self):

        logger.info(
            "Checking whether DDQ access is restricted"
        )

        warning_message = self.page.get_by_text(
            "Access to this page is restricted because due date assignment is automatic in the current system.",
            exact=False
        )

        try:
            warning_message.wait_for(
                state="visible",
                timeout=10000
            )

            logger.warning(
                "DDQ access is restricted because "
                "due date assignment is automatic"
            )

            # Close warning popup
            ok_button = self.page.get_by_role(
                "button",
                name="Ok",
                exact=True
            )

            if ok_button.is_visible():
                ok_button.click()

                logger.info(
                    "DDQ restriction warning closed"
                )

            return True

        except PlaywrightTimeoutError:

            logger.info(
                "DDQ access is available"
            )

            return False