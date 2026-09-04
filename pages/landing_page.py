from playwright.sync_api import Page, expect


class LandingPage:

    def __init__(self, page: Page):

        self.page = page

    def verify_landing_page(self, expected_url):

        expect(self.page).to_have_url(
            expected_url
        )