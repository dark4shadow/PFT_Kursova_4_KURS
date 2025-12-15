from __future__ import annotations

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver, wait_s: float = 10.0):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_s)

    def open(self, url: str):
        with allure.step(f"Open URL: {url}"):
            self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        with allure.step(f"Click: {locator}"):
            el = self.wait.until(EC.element_to_be_clickable(locator))
            el.click()

    def type(self, locator, text: str, *, clear: bool = True):
        with allure.step(f"Type into: {locator}"):
            el = self.wait.until(EC.visibility_of_element_located(locator))
            if clear:
                el.clear()
            el.send_keys(text)

    def text_of(self, locator) -> str:
        el = self.wait.until(EC.visibility_of_element_located(locator))
        return el.text
