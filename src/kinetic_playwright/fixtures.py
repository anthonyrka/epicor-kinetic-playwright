import os
from pathlib import Path

import pytest
from playwright.sync_api import (
    sync_playwright,
    Page,
    Browser,
    BrowserContext,
)

from .config import KineticConfig
from .pages.login import LoginPage

STATE_FILE = Path("epicor_state.json")


def _bool_from_env(name: str, default: str = "true") -> bool:
    raw = os.getenv(name, default).strip().lower()
    return raw in ("true", "1", "yes", "y", "on")


@pytest.fixture(scope="session")
def kp_config() -> KineticConfig:
    """
    Session-scoped configuration loaded from environment variables.

    Required env vars:
      - EPICOR_BASE_URL
      - EPICOR_USERNAME
      - EPICOR_PASSWORD

    Optional:
      - PLAYWRIGHT_HEADLESS
      - PLAYWRIGHT_SLOW_MO_MS
    """
    return KineticConfig.from_env()


@pytest.fixture(scope="session")
def playwright_instance():
    """
    Shared Playwright instance for the entire test session.
    """
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, kp_config: KineticConfig) -> Browser:
    """
    Shared browser instance.

    headless / slow_mo are controlled via env in KineticConfig.
    """
    browser = playwright_instance.chromium.launch(
        headless=kp_config.headless,
        slow_mo=kp_config.slow_mo_ms,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def auth_context(browser: Browser, kp_config: KineticConfig) -> BrowserContext:
    """
    Session-scoped authenticated browser context for Epicor Kinetic.

    Behavior:

    - If EPICOR_REUSE_STATE=true and epicor_state.json exists:
        * Try to reuse it.
        * If we still end up on the login route, treat it as stale and perform
          a fresh login, then overwrite epicor_state.json.
    - If EPICOR_REUSE_STATE=false or the state file does not exist:
        * Always perform a fresh login once per test session.

    In all cases, by the time this fixture yields, the context should be
    authenticated so that navigation to base_url lands on the shell, not login.
    """

    reuse_state = _bool_from_env("EPICOR_REUSE_STATE", default="true")

    def fresh_login() -> BrowserContext:
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(kp_config.base_url, wait_until="networkidle")

        login = LoginPage(page)
        login.login_via_epicor_basic(kp_config.username, kp_config.password)

        # After login we should *not* still be on the login route.
        if "#/login" in page.url:
            raise RuntimeError(
                f"Fresh login did not complete; still on login URL: {page.url}"
            )

        if reuse_state:
            ctx.storage_state(path=str(STATE_FILE))

        # we don't need this page any more; tests get a new page
        page.close()
        return ctx

    ctx: BrowserContext | None = None

    try:
        # First attempt: reuse stored state if enabled + file exists
        if reuse_state and STATE_FILE.exists():
            ctx = browser.new_context(storage_state=str(STATE_FILE))
            page = ctx.new_page()
            page.goto(kp_config.base_url, wait_until="networkidle")

            # If reuse worked, we should *not* be on the login route
            if "#/login" in page.url:
                # stale / invalid -> throw away and do a real login
                page.close()
                ctx.close()
                ctx = fresh_login()
            else:
                # state is good, keep this context
                page.close()
        else:
            # No reuse or no file -> always do a fresh login
            ctx = fresh_login()

        yield ctx

    finally:
        if ctx is not None:
            ctx.close()


@pytest.fixture
def epicor_page(auth_context: BrowserContext, kp_config: KineticConfig) -> Page:
    """
    Per-test fresh page against the Epicor shell (relying on stored auth).

    Typical pattern for tests that want to start from the shell home screen.
    """
    page = auth_context.new_page()
    page.goto(kp_config.base_url, wait_until="networkidle")

    # Defensive: if we somehow land back on login, fail fast instead of
    # silently breaking all tests that assume the shell is visible.
    if "#/login" in page.url:
        raise RuntimeError(
            f"epicor_page fixture ended up on login URL: {page.url}. "
            f"Login likely failed or state is invalid."
        )

    yield page
    page.close()
