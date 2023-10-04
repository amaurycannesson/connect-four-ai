from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    page.goto("http://localhost:8000/")
    expect(page.locator("css=.disc")).to_have_count(42)
