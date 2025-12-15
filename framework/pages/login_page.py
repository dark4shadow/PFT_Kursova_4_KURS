from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

from framework.pages.base_page import BasePage
from framework.pages.locators.login_locators import LoginLocators


class LoginPage(BasePage):
    def open_login(self, base_url: str):
        self.open(base_url)
        return self

    @allure.step("Login with username={username}")
    def login(self, username: str, password: str):
        self.type(LoginLocators.USERNAME, username)
        self.type(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    @allure.step("Login using Selenium Relative Locators")
    def login_with_relative_locators(self, username: str, password: str):
        username_el = self.find(LoginLocators.USERNAME)

        # Selenium 4 feature: relative locators (password input located below username input)
        password_el = self.driver.find_element(
            locate_with(By.TAG_NAME, "input").below(username_el)
        )
        password_el.clear()
        password_el.send_keys(password)

        username_el.clear()
        username_el.send_keys(username)

        login_btn = self.driver.find_element(
            locate_with(By.TAG_NAME, "input").below(password_el)
        )
        login_btn.click()

    def error_message(self) -> str:
        return self.text_of(LoginLocators.ERROR)
