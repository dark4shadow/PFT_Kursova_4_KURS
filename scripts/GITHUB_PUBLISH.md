# Публікація проєкту на GitHub (Windows)

## 1) Підготовка
Перевірте, що у проєкті є `.gitignore` і туди НЕ потрапляють:
- `allure-results/`, `allure-report/`, `tools/allure/`, `.venv/`, `logs/`
- `selenium-server-*.jar` (jar краще не комітити)

## 2) Ініціалізувати git та зробити коміт
У корені проєкту:

```bat
git init
git add .
git commit -m "Initial commit: Selenium cross-browser framework"
```

Якщо git попросить ім’я/пошту:

```bat
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 3) Створити репозиторій на GitHub
На GitHub створіть новий порожній репозиторій (без README/ліцензій).

## 4) Додати remote і запушити

```bat
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

## 5) Перевірка
- відкрийте сторінку репозиторію
- переконайтесь, що є `README.md`, тести і `COURSE_REPORT.md`
