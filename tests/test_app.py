from playwright.sync_api import Page, expect


def test_should_display_empty_grid(page: Page):
    page.goto("http://localhost:8000/")
    expect(page.locator(".disc:not(.preview)")).to_have_count(42)


def test_should_display_red_disk_when_clicking_a_column(page: Page):
    page.goto("http://localhost:8000/")
    last_col = page.locator(".col").locator("nth=-1")
    last_col.click()
    expect(last_col.locator(".disc.R")).to_have_count(1)
