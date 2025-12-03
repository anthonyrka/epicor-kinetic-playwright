from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def wait_for_toast(page: Page, text_substring: str, timeout_ms: int = 5000) -> bool:
    """
    Example helper: wait for a toast/snackbar message containing given text.

    Adjust selectors to match how Kinetic displays status messages.
    """
    try:
        locator = page.get_by_text(text_substring)
        locator.wait_for(timeout=timeout_ms)
        return True
    except PlaywrightTimeoutError:
        return False
