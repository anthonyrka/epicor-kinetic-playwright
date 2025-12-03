from kinetic_playwright.pages.login import LoginPage


def test_login_via_epicor_basic_with_fixtures(browser, kp_config):
    """
    This mimics your working manual test, but:
      - uses the shared Playwright browser fixture
      - uses KineticConfig for base_url / username / password
      - uses the LoginPage page object for the actual steps
    """
    page = browser.new_page()

    # 1) Go to the Epicor shell login
    page.goto(kp_config.base_url, wait_until="networkidle")
    page.wait_for_timeout(3_000)

    # 2–4) Perform the Epicor Basic login flow via the page object
    login = LoginPage(page)
    login.login_via_epicor_basic(kp_config.username, kp_config.password)

    # 5) Assert we are NOT still on the login route
    assert "#/login" not in page.url

    page.close()
