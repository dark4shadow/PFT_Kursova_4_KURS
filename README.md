# Кросбраузерне тестування (Selenium + Pytest + Allure)

## Що реалізовано
- **Page Object Model (POM)**: `LoginPage`, `InventoryPage`, базовий `BasePage`.
- **Factory Pattern**: `DriverFactory` для створення драйвера (Local/Grid).
- **Singleton (керування життєвим циклом)**: pytest fixture `driver` (створює/закриває сесію через `driver.quit()` після тесту).
- **Кросбраузерність**: параметр `--browser=chrome|firefox`.
- **Перемикання середовища**: `--env=local|grid`.
- **Allure**: кроки + вкладення + скріншот при падінні.
- **Selenium 4 feature**: Relative Locators у позитивному тесті.

## Встановлення
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск локально
```bat
pytest --env=local --browser=chrome --alluredir=allure-results
pytest --env=local --browser=firefox --alluredir=allure-results
```

## Звіт Allure
### Варіант A: якщо Allure CLI вже встановлений
```bat
allure serve allure-results
```

### Варіант B: без глобальної інсталяції (Windows)
Скрипт завантажує Allure CLI у `tools/allure/` і генерує HTML у `allure-report/`.

```bat
powershell -ExecutionPolicy Bypass -File scripts\generate_allure_report.ps1
```

Після цього можна відкрити `allure-report/index.html` (або виконати `allure open allure-report`, якщо CLI доступний у PATH).

## Скріншоти при падінні
При падінні тесту скріншот зберігається у папці `screenshots/` і прикріплюється до Allure.

Щоб спеціально згенерувати скріншот (демо), є тест з маркером `demo_fail`.
Він **не запускається за замовчуванням**.

```bat
pytest -m demo_fail --alluredir=allure-results
```

## Запуск через Selenium Grid
Інструкція: [scripts/README_GRID.md](scripts/README_GRID.md)

Примітка: Selenium Grid 4 потребує Java 11+ (перевірка: `java -version`).

Приклад:
```bat
pytest --env=grid --browser=chrome --grid-url=http://localhost:4444/wd/hub --alluredir=allure-results
```
