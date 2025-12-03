from playwright.sync_api import Page


class LoginPage:
    """
    Page object for the Epicor Kinetic login screen.

    This version explicitly performs the "Epicor Basic" login flow:
      - Select "Epicor Basic" from the "User Account Type" dropdown
      - Fill username + password
      - Click "Log in"
    """

    def __init__(self, page: Page):
        self.page = page

    def login_via_epicor_basic(self, username: str, password: str) -> None:
        page = self.page

        # Make sure the login page is fully idle before we start poking it
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3_000)

        # 1) Open "User Account Type" dropdown and pick "Epicor Basic"
        dropdown = page.get_by_label("User Account Type")
        dropdown.click()

        option = page.get_by_role("option", name="Epicor Basic")
        option.click()

        # 2) Fill username & password (using the same selectors that worked)
        username_input = page.locator("input#input_username")
        password_input = page.locator("input#input_password")

        username_input.fill(username)
        password_input.fill(password)

        # 3) Click "Log in" button
        login_button = page.get_by_role("button", name="Log in")
        login_button.click()

        # 4) Wait for the shell to load
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5_000)

    def login(self, username: str, password: str) -> None:
        """
        Generic login entrypoint used by fixtures.

        For now this *always* uses the Epicor Basic path, because that's the
        one we know works in your tenant.
        """
        self.login_via_epicor_basic(username, password)

    def is_on_login_page(self) -> bool:
        """
        Helper if you ever want to assert we’re still on the login route.
        """
        url = self.page.url or ""
        return "#/login" in url or "authMethod=idp" in url
