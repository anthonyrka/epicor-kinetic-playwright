# Getting Started

This guide walks you through getting `epicor-kinetic-playwright` running
against your own Epicor Kinetic environment.

---

## 1. Prerequisites

- Python 3.10+ installed
- Git installed
- Access to an Epicor Kinetic environment (e.g., **Third / Test / Pilot**)
- A test user account that can log into Kinetic

---

## 2. Clone and create a virtual environment

```bash
git clone https://github.com/<your-gh-user>/epicor-kinetic-playwright.git
cd epicor-kinetic-playwright

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

## 3. Install dependencies

```bash
pip install -e .
python -m playwright install
```

This installs:
- Playwright browser automation for Python
- Pytest for running tests
- python-dotenv for loading .env configuration

## 4. Configure environment variables

```bash
cp .env.example .env
```

Tips:
- Use a non-production environment where possible.
- Use a dedicated test user account with appropriate permissions.


## 5. Run the tests

```bash
pytest -v
```
If selectors in login.py and the shell assertions in test_login.py match
your tenant, you should see the tests:
- Start a browser
- Log in to Kinetic
- Run a small set of checks

If tests fail with selector-related errors, proceed to the next section.

## 6. Adjusted selectors for your tenant

Different Kinetic deployments may have:
- Different labels for user ID / password
- Different sign-in button text
- Different shell layout and menu labels

Start by updating:
- src/kinetic_playwright/pages/login.py
- src/kinetic_playwright/pages/shell.py

Use one of these approaches:

1. Playwright Codegen

```bash
python -m playwright codegen https://your-tenant.epicorsaas.com/server/apps/erp/home
```
- Log in manually and open a few screens.
- Look at the generated Python code to see which selectors work.
- Copy and simplify the useful selectors into your page objects.

2. Playwright Inspector
Run tests with PWDEBUG=1 to inspect the DOM during execution:

```bash
PYTHONPATH=src pytest tests/e2e/test_login_basic_flow.py -vv
```

Use the inspector to experiment with selectors, then update login.py
and shell.py accordingly.

## 7. Next steps
Once the basic login and shell tests are stable:
- Add or adapt page objects for specific screens (e.g., Customer Entry).
- Write tests that exercise your customizations:
-- custom fields
-- UD table data
-- BAQ-driven grids
-- BPM-based validation

See `docs/writing-tests.md` for patterns and examples.