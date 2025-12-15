# Selenium Grid 4 (без Docker) — запуск на Windows

## Передумови
- Встановлений Java (JDK/JRE 11+). (Selenium Grid 4 зазвичай потребує Java 11 або новіше.)
- Встановлені браузери Chrome та Firefox.
- Завантажений `selenium-server-<version>.jar`.

Рекомендовано покласти файл у корінь проєкту (поруч з `requirements.txt`) або в папку `scripts/`.

> Цей проєкт розрахований на Grid у режимі Hub + 2 Nodes (Chrome/Firefox).

## 1) Запуск Hub
У папці з `.jar` виконайте:

```bat
java -jar selenium-server-4.x.x.jar hub
```

Після запуску Hub у логах будуть порти Event Bus (типово 4442/4443) і URL консолі Grid: `http://localhost:4444/`.

## 2) Запуск Node (Chrome)
В іншому вікні термінала:

```bat
java -jar selenium-server-4.x.x.jar node --port 5555 --detect-drivers true --publish-events tcp://localhost:4442 --subscribe-events tcp://localhost:4443
```

## 3) Запуск Node (Firefox)
В іншому вікні термінала:

```bat
java -jar selenium-server-4.x.x.jar node --port 5556 --detect-drivers true --publish-events tcp://localhost:4442 --subscribe-events tcp://localhost:4443
```

## 4) Перевірка
Відкрийте `http://localhost:4444/ui` і переконайтесь, що є 2 ноди.

## 5) Запуск тестів через Grid
З кореня проєкту:

```bat
pytest --env=grid --browser=chrome --grid-url=http://localhost:4444/wd/hub --alluredir=allure-results
pytest --env=grid --browser=firefox --grid-url=http://localhost:4444/wd/hub --alluredir=allure-results
```

## Troubleshooting
- Якщо при старті `.jar` бачите `UnsupportedClassVersionError` (наприклад, class file version 55.0) — у вас Java 8. Встановіть Java 11+ і перевірте `java -version`.
