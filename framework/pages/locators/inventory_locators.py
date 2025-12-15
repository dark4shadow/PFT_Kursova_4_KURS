from selenium.webdriver.common.by import By


class InventoryLocators:
    TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
