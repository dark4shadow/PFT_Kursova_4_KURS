from __future__ import annotations

import allure

from framework.pages.base_page import BasePage
from framework.pages.locators.inventory_locators import InventoryLocators


class InventoryPage(BasePage):
    @allure.step("Verify inventory page opened")
    def is_opened(self) -> bool:
        self.find(InventoryLocators.INVENTORY_CONTAINER)
        title = self.text_of(InventoryLocators.TITLE)
        return title.strip().lower() == "products"
