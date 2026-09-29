from playwright.sync_api import Locator, Page, expect


class WaitUtils:

    DEFAULT_TIMEOUT = 30000

    @staticmethod
    def wait_for_visible(
        locator: Locator,
        timeout: int = DEFAULT_TIMEOUT
    ):
        expect(locator).to_be_visible(
            timeout=timeout
        )

    @staticmethod
    def wait_for_hidden(
        locator: Locator,
        timeout: int = DEFAULT_TIMEOUT
    ):
        expect(locator).to_be_hidden(
            timeout=timeout
        )

    @staticmethod
    def wait_for_enabled(
        locator: Locator,
        timeout: int = DEFAULT_TIMEOUT
    ):
        expect(locator).to_be_enabled(
            timeout=timeout
        )

    @staticmethod
    def wait_for_attached(
        locator: Locator,
        timeout: int = DEFAULT_TIMEOUT
    ):
        locator.wait_for(
            state="attached",
            timeout=timeout
        )

    @staticmethod
    def wait_for_url(
        page: Page,
        url: str,
        timeout: int = DEFAULT_TIMEOUT
    ):
        page.wait_for_url(
            url,
            timeout=timeout
        )