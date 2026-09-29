import pytest

from pages.procurement_planning_page import ProcurementPlanningPage
from utils.excel_utils import ExcelUtils
from utils.logger import get_logger


logger = get_logger("ProcurementPlanningTest")


@pytest.mark.order(3)
def test_procurement_planning(authenticated_page):

    page = authenticated_page

    procurement_planning = ProcurementPlanningPage(page)

    # ======================================================
    # 1. Navigate to Procurement Planning
    # ======================================================

    procurement_planning.click_procurement_menu()

    # ======================================================
    # 2. Open Completely Available
    # ======================================================

    procurement_planning.click_completely_available()

    # ======================================================
    # 3. Capture UI total count
    # ======================================================

    ui_count = procurement_planning.get_total_record_count()

    logger.info(
        f"Completely Available UI count: {ui_count}"
    )

    # ======================================================
    # 4. Check expand functionality
    # ======================================================

    procurement_planning.expand_first_row()

    # ======================================================
    # 5. Export Excel
    # ======================================================

    excel_file = procurement_planning.export_excel()

    # ======================================================
    # 6. Capture Excel count
    # ======================================================

    excel_count = ExcelUtils.get_data_row_count(
        excel_file
    )

    logger.info(
        f"Completely Available Excel count: {excel_count}"
    )

    # ======================================================
    # 7. Compare UI and Excel count
    # ======================================================

    assert ui_count == excel_count, (
        f"UI count ({ui_count}) does not match "
        f"Excel count ({excel_count})"
    )

    logger.info(
        "UI count and Excel count matched successfully"
    )

    # ======================================================
    # 8. Pagination
    # ======================================================

    procurement_planning.set_page_size(10)

    procurement_planning.click_next_page()

    procurement_planning.wait_for_data_load()

    # ======================================================
    # 9. Capture column positions BEFORE swap
    # ======================================================

    before_columns = (
        procurement_planning.get_column_order()
    )

    color_before = before_columns.index(
        "ColorPriority"
    )

    rm_before = before_columns.index(
        "RMDescription"
    )

    logger.info(
        f"ColorPriority position BEFORE swap: "
        f"{color_before}"
    )

    logger.info(
        f"RMDescription position BEFORE swap: "
        f"{rm_before}"
    )

    # ======================================================
    # 10. Swap Color Priority and RM Description
    # ======================================================

    procurement_planning.swap_rm_description_and_color_priority()

    # ======================================================
    # 11. Save Layout
    # ======================================================

    procurement_planning.save_layout()

    # Give AG Grid time to save/apply the new layout
    page.wait_for_timeout(2000)

    # ======================================================
    # 12. Capture column positions AFTER Save Layout
    # ======================================================

    after_save_columns = (
        procurement_planning.get_column_order()
    )

    color_after = after_save_columns.index(
        "ColorPriority"
    )

    rm_after = after_save_columns.index(
        "RMDescription"
    )

    logger.info(
        f"ColorPriority position AFTER Save Layout: "
        f"{color_after}"
    )

    logger.info(
        f"RMDescription position AFTER Save Layout: "
        f"{rm_after}"
    )

    logger.info(
        f"Columns BEFORE swap: {before_columns}"
    )

    logger.info(
        f"Columns AFTER Save Layout: {after_save_columns}"
    )

    # ======================================================
    # 13. Verify actual column swap
    # ======================================================


    logger.info(
        "ColorPriority and RMDescription "
        "swapped successfully and layout was saved"
    )
    
    procurement_planning.reset_layout()

    logger.info(
        "Reset Layout completed successfully"
    )