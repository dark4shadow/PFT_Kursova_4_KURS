import allure

from framework.pages.inventory_page import InventoryPage
from framework.pages.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("Positive login")
def test_positive_login(driver, run_config):
    login = LoginPage(driver, wait_s=run_config.explicit_wait_s).open_login(run_config.base_url)

    # Demonstrate Selenium 4 relative locators
    login.login_with_relative_locators("standard_user", "secret_sauce")

    inventory = InventoryPage(driver, wait_s=run_config.explicit_wait_s)
    assert inventory.is_opened(), "Inventory page did not open after valid login"


@allure.feature("Authentication")
@allure.story("Negative login")
def test_negative_login_locked_user(driver, run_config):
    login = LoginPage(driver, wait_s=run_config.explicit_wait_s).open_login(run_config.base_url)

    login.login("locked_out_user", "secret_sauce")

    msg = login.error_message().lower()
    assert "locked out" in msg, f"Unexpected error message: {msg}"
