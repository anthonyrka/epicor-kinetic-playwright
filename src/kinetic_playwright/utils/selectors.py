from playwright.sync_api import Page


def click_button_by_text(page: Page, text: str):
    """
    Convenience helper for clicking a button with a given visible name.
    """
    page.get_by_role("button", name=text).click()
