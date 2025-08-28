import os
import warnings
from dataclasses import dataclass
from datetime import timezone

import pandas as pd

from .section import Section
from .ui import UI
from .widget import Widget


@dataclass
class ONCDW:
    token: str | None = None
    env: str = "PROD"  # "PROD" | "QA"
    showInfo: bool = False

    def __post_init__(self):
        if self.token is None:
            self.token = os.environ.get("ONC_TOKEN")
            if self.token is None:
                raise ValueError(
                    "Please set token by passing token to the ONCDW class or by setting the ONC_TOKEN environment variable"
                )

        self.widget = Widget(self)
        self.now = self._now()
        self.section = Section(self)
        self.ui = UI()

    @property
    def hostname(self) -> str:
        if self.env.upper() == "QA":
            return "qa.oceannetworks.ca"
        elif self.env.upper() != "PROD":
            warnings.warn(
                f"Env {self.env} is not in (PROD, QA), default to PROD.", stacklevel=2
            )
        return "data.oceannetworks.ca"

    def _now(self):
        return pd.Timestamp.now(timezone.utc).tz_localize(None)
