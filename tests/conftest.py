import pytest
from playwright.sync_api import sync_playwright
from src.pages.dashboard_page import DashboardPage
from src.api_client import PumpApiClient

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    return DashboardPage(page)

@pytest.fixture(scope="session")
def api_client() -> PumpApiClient:
    return PumpApiClient()