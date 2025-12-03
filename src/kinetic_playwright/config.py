import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from a .env file if present.
# This runs when the module is imported.
load_dotenv()


@dataclass
class KineticConfig:
    """
    Configuration for connecting to an Epicor Kinetic environment.
    Values are loaded from environment variables.

    Required:
      - EPICOR_BASE_URL
      - EPICOR_USERNAME
      - EPICOR_PASSWORD

    Optional:
      - PLAYWRIGHT_HEADLESS (default: "true")
      - PLAYWRIGHT_SLOW_MO_MS (default: "0")
      - EPICOR_REUSE_STATE  (default: "true")
    """

    base_url: str
    username: str
    password: str
    headless: bool = True
    slow_mo_ms: int = 0
    reuse_state: bool = True  # <--- NEW

    @classmethod
    def from_env(cls) -> "KineticConfig":
        base_url = os.environ.get("EPICOR_BASE_URL")
        username = os.environ.get("EPICOR_USERNAME")
        password = os.environ.get("EPICOR_PASSWORD")

        if not base_url or not username or not password:
            missing = [
                name
                for name, value in [
                    ("EPICOR_BASE_URL", base_url),
                    ("EPICOR_USERNAME", username),
                    ("EPICOR_PASSWORD", password),
                ]
                if not value
            ]
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Set them in your environment or .env file."
            )

        headless_raw = os.environ.get("PLAYWRIGHT_HEADLESS", "true").strip().lower()
        headless = headless_raw in ("true", "1", "yes", "y", "on")

        slow_mo_raw = os.environ.get("PLAYWRIGHT_SLOW_MO_MS", "0").strip()
        try:
            slow_mo_ms = int(slow_mo_raw)
        except ValueError:
            raise RuntimeError(
                f"PLAYWRIGHT_SLOW_MO_MS must be an integer; got {slow_mo_raw!r}"
            )

        reuse_raw = os.environ.get("EPICOR_REUSE_STATE", "true").strip().lower()
        reuse_state = reuse_raw in ("true", "1", "yes", "y", "on")

        return cls(
            base_url=base_url,
            username=username,
            password=password,
            headless=headless,
            slow_mo_ms=slow_mo_ms,
            reuse_state=reuse_state,
        )
