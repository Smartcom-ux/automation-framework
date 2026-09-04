import pytest

from api.auth_api import AuthAPI
from config.settings import Settings


def pytest_addoption(parser):

    parser.addoption(
        "--env",
        action="store",
        default="lab1",
        help="Environment to execute tests"
    )


@pytest.fixture(scope="session")
def settings(request):

    environment = request.config.getoption("--env")

    return Settings(environment)


@pytest.fixture
def authenticated_page(browser, settings):

    # --------------------------------
    # 1. Validate credentials
    # --------------------------------

    if not settings.username:
        pytest.fail(
            "VFST_USERNAME environment variable is not configured."
        )

    if not settings.password:
        pytest.fail(
            "VFST_PASSWORD environment variable is not configured."
        )

    # --------------------------------
    # 2. Create browser context
    # --------------------------------

    context = browser.new_context()

    try:

        # --------------------------------
        # 3. Login through API
        # --------------------------------

        auth_api = AuthAPI(context)

        response = auth_api.login(
            login_url=settings.login_url,
            username=settings.username,
            password=settings.password
        )

        # --------------------------------
        # 4. Validate API response
        # --------------------------------

        assert response.status == 200, (
            f"Login API failed. "
            f"Status={response.status}, "
            f"Response={response.text()}"
        )

        response_data = response.json()

        assert response_data.get("data", {}).get("msg") == "Login successful", (
            f"Login was not successful. "
            f"Response={response_data}"
        )

        # --------------------------------
        # 5. Validate access_token cookie
        # --------------------------------

        cookies = context.cookies()

        cookie_names = {
            cookie["name"]
            for cookie in cookies
        }

        assert "access_token" in cookie_names, (
            "Login successful but access_token "
            "cookie was not received."
        )

        # --------------------------------
        # 6. Create authenticated page
        # --------------------------------

        page = context.new_page()

        # --------------------------------
        # 7. Open application
        # --------------------------------

        page.goto(
            settings.base_url,
            wait_until="domcontentloaded"
        )

        yield page

    finally:

        context.close()