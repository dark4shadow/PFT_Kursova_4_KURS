## 1. Мета та об’єкт дослідження

**Мета роботи** — розробити програмне рішення (автоматизований фреймворк) для кросбраузерного UI end-to-end тестування веб‑додатку в браузерах Chrome та Firefox з використанням Selenium WebDriver, Pytest, Allure та Selenium Grid.

**Об’єкт тестування:** веб‑ресурс https://www.saucedemo.com/ (Swag Labs).

**Тип тестування:** UI End‑to‑End (Black Box).

---

## 2. Технічне завдання (узагальнення)

В рамках практичної частини реалізовано фреймворк, який забезпечує:

- запуск тестів у двох браузерах (Chrome/Firefox);
- режим виконання `local` або `grid` (Selenium Grid 4); 
- застосування патернів: **Page Object Model (POM)**, **Factory**, керування життєвим циклом драйвера через **pytest fixtures**;
- формування звітів Allure зі кроками та вкладеннями;
- автоматичне збереження скріншота при падінні тесту;
- демонстрацію Selenium 4 feature: **Relative Locators**.

---

## 3. Технологічний стек

- Мова: Python 3.10+ (фактично використано Python 3.12)
- Selenium WebDriver 4.x
- Pytest
- Selenium Grid 4 (Hub + Nodes, запуск через `.jar` без Docker)
- Allure Reports (Allure Pytest + Allure Commandline для HTML)

Файл залежностей: [requirements.txt](requirements.txt)

---

## 4. Архітектура та патерни

### 4.1. Page Object Model (POM)

Сторінки веб‑додатку реалізовані у вигляді класів:

- [framework/pages/login_page.py](framework/pages/login_page.py)
- [framework/pages/inventory_page.py](framework/pages/inventory_page.py)

Локатори винесені окремо:

- [framework/pages/locators/login_locators.py](framework/pages/locators/login_locators.py)
- [framework/pages/locators/inventory_locators.py](framework/pages/locators/inventory_locators.py)

Базовий клас із “обгортками” для типових операцій Selenium:

- [framework/pages/base_page.py](framework/pages/base_page.py)

### 4.2. Factory Pattern (DriverFactory)

Створення драйвера централізовано у фабриці:

- [framework/driver_factory.py](framework/driver_factory.py)

Фабрика підтримує параметри:

- `browser`: `chrome` або `firefox`
- `env`: `local` або `grid`
- `grid_url`: URL Selenium Grid (наприклад `http://localhost:4444/wd/hub`)
- `headless`: запуск без UI

### 4.3. Керування життєвим циклом (pytest fixtures)

Життєвий цикл WebDriver керується fixture `driver` зі scope=`function`, що гарантує `driver.quit()` після кожного тесту:

- [tests/conftest.py](tests/conftest.py)

Також у `conftest.py` реалізовано:

- параметризацію CLI (`--browser`, `--env`, `--grid-url`, `--base-url`, `--headless`);
- hook `pytest_runtest_makereport` для створення скріншота і прикріплення до Allure при падінні.

---

## 5. Реалізовані тестові сценарії

Тести розташовані у файлі:

- [tests/test_login.py](tests/test_login.py)

### 5.1. Позитивний сценарій входу

- Логін: `standard_user`
- Пароль: `secret_sauce`
- Перевірка: після входу відкривається сторінка товарів (`Products`).

Додатково продемонстровано Selenium 4 feature: **Relative Locators** (пошук поля паролю відносно поля логіну).

### 5.2. Негативний сценарій входу

- Логін: `locked_out_user`
- Пароль: `secret_sauce`
- Перевірка: відображається повідомлення про помилку з текстом про блокування.

---

## 6. Налаштування та запуск

### 6.1. Встановлення

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 6.2. Запуск локально

```bat
pytest --env=local --browser=chrome --alluredir=allure-results
pytest --env=local --browser=firefox --alluredir=allure-results
```

### 6.3. Запуск Selenium Grid (без Docker)

Інструкція: [scripts/README_GRID.md](scripts/README_GRID.md)

Ключова вимога: **Java 11+** (перевірка `java -version`).

Після запуску Hub та Nodes можна виконати:

```bat
pytest --env=grid --browser=chrome --grid-url=http://localhost:4444/wd/hub --alluredir=allure-results
pytest --env=grid --browser=firefox --grid-url=http://localhost:4444/wd/hub --alluredir=allure-results
```

---

## 7. Звітність Allure

Результати тестів записуються в `allure-results/`.

HTML‑звіт генерується у `allure-report/`.

### Генерація HTML без глобальної інсталяції Allure

```bat
powershell -ExecutionPolicy Bypass -File scripts\generate_allure_report.ps1
```

Скрипт: [scripts/generate_allure_report.ps1](scripts/generate_allure_report.ps1)

---

## 8. Результати експериментів

У ході перевірки виконано прогони в двох браузерах у двох режимах:

- **Local / Chrome** — успішно
- **Local / Firefox** — успішно
- **Grid / Chrome** — успішно
- **Grid / Firefox** — успішно

Отримано Allure‑звіт (HTML) із кроками та вкладеннями.

---

## 9. Висновки

У практичній частині курсової роботи реалізовано фреймворк автоматизованого кросбраузерного тестування на основі Selenium WebDriver та Pytest. Забезпечено масштабування запусків через Selenium Grid, застосовано POM та Factory для покращення підтримуваності коду, а також інтегровано Allure‑звітність для аналізу результатів тестування.

---

## Додаток А. Структура проєкту

Ключові модулі:

- [framework/driver_factory.py](framework/driver_factory.py)
- [framework/pages/base_page.py](framework/pages/base_page.py)
- [framework/pages/login_page.py](framework/pages/login_page.py)
- [framework/pages/inventory_page.py](framework/pages/inventory_page.py)
- [tests/test_login.py](tests/test_login.py)

---

## Додаток B. Публікація на GitHub (коротко)

1) Ініціалізація репозиторію та перший коміт:

```bat
git init
git add .
git commit -m "Initial commit: Selenium cross-browser test framework"
```

2) Створити порожній репозиторій на GitHub та під’єднати remote:

```bat
git remote add origin https://github.com/<user>/<repo>.git
git branch -M main
git push -u origin main
```

Далі вказати URL репозиторію тут: _https://github.com/<user>/<repo>_
