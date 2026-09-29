from pages.due_date_calculation_page import DueDateCalculationPage
import pytest


@pytest.mark.order(4)
def test_due_date_calculation_page(authenticated_page):

    page = authenticated_page
    
    due_date_calculation = DueDateCalculationPage(page)

    due_date_calculation.due_date_calculation()
    
 

    if due_date_calculation.check_access_restriction():
        pytest.skip(
            "DDQ skipped: Due date assignment is automatic "
            "in the current system"
        )

    due_date_calculation.select_order()
    due_date_calculation.click_continue()
    due_date_calculation.select_order_after_continue()  
    due_date_calculation.click_edit()
    due_date_calculation.select_ddq_dropdowns(0)
    due_date_calculation.select_ddq_dropdowns(1)
    due_date_calculation.select_ddq_dropdowns(2)
    due_date_calculation.select_ddq_dropdowns(3)
    due_date_calculation.click_save()
    due_date_calculation.click_calculate_due_date()
    due_date_calculation.click_confirm()
    due_date_calculation.click_schedule()    
    
    schedule_message = (
    due_date_calculation.capture_schedule_toast()
) 

    print(
    f"Final Schedule Message: {schedule_message}"
)
    
    