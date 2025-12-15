import allure
import pytest

from framework.pages.inventory_page import InventoryPage
from framework.pages.login_page import LoginPage


@allure.feature("Reporting")
@allure.story("Demo screenshot on failure")
@pytest.mark.demo_fail
def test_demo_screenshot_on_failure(driver, run_config):
    """Intentionally fails to demonstrate screenshot + Allure attachment."""

    login = LoginPage(driver, wait_s=run_config.explicit_wait_s).open_login(run_config.base_url)

    # This user is expected to be blocked.
    login.login("locked_out_user", "secret_sauce")

    # Intentionally wrong expectation: inventory page should open.
    inventory = InventoryPage(driver, wait_s=run_config.explicit_wait_s)
    assert inventory.is_opened(), "DEMO: expected inventory page (should fail and produce screenshot)"
