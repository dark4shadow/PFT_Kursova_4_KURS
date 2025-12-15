from __future__ import annotations

import os
from datetime import datetime

import allure
import pytest

from framework.config import RunConfig
from framework.driver_factory import DriverFactory


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--browser", action="store", default="chrome", help="chrome|firefox")
    parser.addoption("--env", action="store", default="local", help="local|grid")
    parser.addoption("--base-url", action="store", default="https://www.saucedemo.com/")
    parser.addoption("--grid-url", action="store", default="http://localhost:4444/wd/hub")
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption("--implicit-wait", action="store", default="0")
    parser.addoption("--explicit-wait", action="store", default="10")


@pytest.fixture(scope="session")
def run_config(request: pytest.FixtureRequest) -> RunConfig:
    return RunConfig(
        base_url=str(request.config.getoption("--base-url")),
        env=str(request.config.getoption("--env")),
        browser=str(request.config.getoption("--browser")),
        grid_url=str(request.config.getoption("--grid-url")),
        headless=bool(request.config.getoption("--headless")),
        implicit_wait_s=float(request.config.getoption("--implicit-wait")),
        explicit_wait_s=float(request.config.getoption("--explicit-wait")),
    )


@pytest.fixture(scope="function")
def driver(run_config: RunConfig, request: pytest.FixtureRequest):
    driver = DriverFactory.create_driver(
        browser=run_config.browser,
        env=run_config.env,
        grid_url=run_config.grid_url,
        headless=run_config.headless,
    )

    driver.implicitly_wait(run_config.implicit_wait_s)

    # Attach browser info to Allure report
    with allure.step("Session info"):
        allure.attach(run_config.browser, name="browser", attachment_type=allure.attachment_type.TEXT)
        allure.attach(run_config.env, name="env", attachment_type=allure.attachment_type.TEXT)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    if rep.failed:
        os.makedirs("screenshots", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshots/{item.name}_{ts}.png"

        try:
            driver.save_screenshot(file_name)
        except Exception:
            return

        try:
            with open(file_name, "rb") as f:
                allure.attach(f.read(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
