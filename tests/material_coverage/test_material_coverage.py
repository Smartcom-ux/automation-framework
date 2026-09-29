from math import ceil
from pathlib import Path

import pytest

from api.material_coverage_api import MaterialCoverageAPI
from pages.material_coverage_page import MaterialCoveragePage
from utils.excel_utils import ExcelUtils
from utils.logger import get_logger


logger = get_logger("MaterialCoverageTest")


@pytest.mark.order(2)
def test_material_coverage_for_open_sales(
    authenticated_page,
    settings
):

    page = authenticated_page

    material_coverage = MaterialCoveragePage(page)

    # ==================================================
    # 1. Open Material Coverage
    # ==================================================

    material_coverage.open_material_coverage()

    # ==================================================
    # 2. Current Coverage
    # ==================================================

    material_coverage.click_current_coverage()

    material_coverage.capture_page_screenshot(
        "01_current_coverage"
    )

    # ==================================================
    # 3. Future Coverage
    # ==================================================

    material_coverage.click_future_coverage()

    material_coverage.capture_page_screenshot(
        "02_future_coverage"
    )

    # ==================================================
    # 4. Click Purple Arrow
    # ==================================================

    material_coverage.click_menu_arrow()

    material_coverage.capture_page_screenshot(
        "03_after_menu_arrow"
    )

    # ==================================================
    # 5. Show All Orders
    # ==================================================

    material_coverage.click_show_all_orders()

    # ==================================================
    # 6. Print ALL Main Grid Columns
    #    WITHOUT Expansion
    # ==================================================

    before_expand_columns = (
        material_coverage.print_all_grid_columns(
            "MAIN GRID COLUMNS - WITHOUT EXPANSION"
        )
    )

    # ==================================================
    # 7. Expand First Order
    # ==================================================

    material_coverage.expand_first_order()

    # ==================================================
    # 8. Print ONLY Expanded Grid Columns
    #    Raw Material Details
    # ==================================================

    expanded_columns = (
        material_coverage.print_expanded_grid_columns()
    )

    # ==================================================
    # 9. Backend / API Count
    # ==================================================

    api = MaterialCoverageAPI(
        page.context
    )

    response = api.get_open_so_details(
        settings.open_so_details_url
    )

    assert response.status == 200, (
        f"API failed. "
        f"Status={response.status}, "
        f"Response={response.text()}"
    )

    response_data = response.json()

    api_count = response_data["data"]["count"]

    logger.info(
        f"API Total Orders: {api_count}"
    )

    # ==================================================
    # 10. Set Page Size = 100
    # ==================================================

    page_size = 100

    material_coverage.set_page_size(
        page_size
    )

    logger.info(
        f"Page Size: {page_size}"
    )

    # ==================================================
    # 11. Validate Pagination
    #     Maximum 4 Next clicks
    # ==================================================

    max_pagination_clicks = 4

    total_pages = ceil(
        api_count / page_size
    )

    # From page 1, valid Next clicks are total_pages - 1
    pagination_clicks = min(
        max_pagination_clicks,
        max(0, total_pages - 1)
    )

    logger.info(
        f"Total Pagination Pages: {total_pages}"
    )

    logger.info(
        f"Validating pagination with "
        f"{pagination_clicks} Next Page clicks"
    )

    for click_number in range(
        1,
        pagination_clicks + 1
    ):

        material_coverage.click_next_page()

        logger.info(
            f"Next Page click "
            f"{click_number}/{pagination_clicks} completed"
        )

    logger.info(
        "Pagination validation completed successfully"
    )

    # ==================================================
    # 12. Column Swap - Log Before
    # ==================================================

    before_columns = (
        material_coverage.get_column_names()
    )

    logger.info(
        "========== COLUMNS BEFORE SWAP =========="
    )

    for index, column in enumerate(
        before_columns
    ):
        logger.info(
            f"{index}: {column}"
        )

    # ==================================================
    # 13. Swap Columns
    # ==================================================

    material_coverage.swap_columns(
        "Color Priority",
        "Order No"
    )

    # ==================================================
    # 14. Column Swap - Log After
    # ==================================================

    after_columns = (
        material_coverage.get_column_names()
    )

    logger.info(
        "========== COLUMNS AFTER SWAP =========="
    )

    for index, column in enumerate(
        after_columns
    ):
        logger.info(
            f"{index}: {column}"
        )

    logger.info(
        "Column swap operation completed."
    )

    # ==================================================
    # 15. Save
    # ==================================================

    material_coverage.click_save()

    # ==================================================
    # 16. Validate Toast
    # ==================================================

    toast_message = (
        material_coverage.get_toast_message()
    )

    logger.info(
        f"Save toast: {toast_message}"
    )

    assert toast_message, (
        "Save toast was not displayed."
    )

    # ==================================================
    # 17. Excel Export
    # ==================================================
  # ==================================================
# 17. Excel Export
# ==================================================

    file_path = material_coverage.export_excel()

    logger.info(
        f"Excel downloaded to: {file_path}"
    )

# ==================================================
# 18. Excel Row Count
    # ==================================================

    excel_count = (
        ExcelUtils.get_row_count(
            file_path
        )
    )

    logger.info(
        f"Excel Total Records: {excel_count}"
    )

    # ==================================================
    # 19. Backend vs Excel Count
    # ==================================================

    assert excel_count == api_count, (
        f"API count = {api_count}, "
        f"Excel records = {excel_count}"
    )

    logger.info(
        "API count and Excel count matched successfully"
    )
    # ==================================================
    # 20. Backend vs Excel Count
    # ==================================================

    assert excel_count == api_count, (
        f"API count = {api_count}, "
        f"Excel records = {excel_count}"
    )

    logger.info(
        "API count and Excel count matched successfully"
    )