import os

import pytest
from dotenv import load_dotenv

from oncdw import ONCDW

load_dotenv(".streamlit/secrets.toml", override=True)
token = os.getenv("ONC_TOKEN")
env = os.getenv("ONC_ENV", "PROD")

def pytest_configure():
    print("========== Config ==========")
    print(f"Testing environment: {env}")

@pytest.fixture()
def client() -> ONCDW:
    return ONCDW(token, env, showInfo=True)
