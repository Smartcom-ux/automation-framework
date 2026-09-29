from pages.landing_page import LandingPage
import pytest

@pytest.mark.order(1)

def test_login_success(authenticated_page, settings):

    landing_page = LandingPage(
        authenticated_page
    )

    expected_url = (
        settings.base_url
        + settings.landing_page
    )

    landing_page.verify_landing_page(
        expected_url
    )