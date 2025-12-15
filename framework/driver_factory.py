from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class DriverFactory:
    @staticmethod
    def create_driver(*, browser: str, env: str, grid_url: str, headless: bool):
        browser_norm = (browser or "").strip().lower()
        env_norm = (env or "").strip().lower()

        if browser_norm not in {"chrome", "firefox"}:
            raise ValueError(f"Unsupported browser: {browser!r}. Use chrome|firefox")
        if env_norm not in {"local", "grid"}:
            raise ValueError(f"Unsupported env: {env!r}. Use local|grid")

        if browser_norm == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            return DriverFactory._create(browser_norm, env_norm, grid_url, options)

        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        return DriverFactory._create(browser_norm, env_norm, grid_url, options)

    @staticmethod
    def _create(browser: str, env: str, grid_url: str, options):
        if env == "local":
            if browser == "chrome":
                return webdriver.Chrome(options=options)
            return webdriver.Firefox(options=options)

        # Selenium Grid 4: RemoteWebDriver with Options (W3C capabilities)
        return webdriver.Remote(command_executor=grid_url, options=options)
