from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


def test_filter_updates_kpi(page: Page):

    page.goto(BASE_URL)

    page.wait_for_selector("text=Average Trip Time")

    # interact with slider
    page.keyboard.press("ArrowRight")

    # verify KPI appears
    expect(page.locator("text=mins")).to_be_visible()


def test_ai_tab_renders_table(page: Page):

    page.goto(BASE_URL)

    page.get_by_text("AI Insights").click()

    expect(page.locator("text=AI Filtered Data")).to_be_visible()


def test_reset_button_clears_filters(page: Page):

    page.goto(BASE_URL)

    page.get_by_text("Reset filter").click()

    expect(page.get_by_role("checkbox", name="Subscriber")).to_be_checked()