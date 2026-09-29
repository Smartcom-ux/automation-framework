from playwright.sync_api import Page, expect

from utils.logger import get_logger


logger = get_logger("LandingPage")


class LandingPage:

    def __init__(self, page: Page):
        self.page = page

    def verify_landing_page(self, expected_url):

        logger.info(
            f"Verifying landing page URL. "
            f"Expected URL: {expected_url}"
        )

        expect(self.page).to_have_url(
            expected_url
        )

        logger.info(
            f"Landing page URL verified successfully: "
            f"{self.page.url}"
        )