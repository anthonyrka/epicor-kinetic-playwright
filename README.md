# epicor-kinetic-playwright

> Community test harness for browser-based automated testing of Epicor Kinetic customizations using Python + Playwright.

**Not affiliated with or endorsed by Epicor Software Corporation.**

## Features

- Python + Playwright scaffolding for Kinetic
- Reusable pytest fixtures (`epicor_page`, `auth_context`)
- Example page objects (login, shell, sample business screen)
- Environment-variable driven configuration
- Example GitHub Actions CI workflow

## Quickstart

```bash
git clone git@github.com:anthonyrka/epicor-kinetic-playwright.git
cd epicor-kinetic-playwright

python -m venv .venv
source .venv/bin/activate

pip install -e .
python -m playwright install

cp .env.example .env
# edit .env with your tenant URL and credentials

pytest -v

```

or:

```bash
PYTHONPATH=src pytest tests/e2e/test_login_basic_flow.py -vv
```

