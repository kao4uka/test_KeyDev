# Django приложение «Учёт баланса по МСФО 9»

Простое Django-приложение для ведения бухгалтерского учёта в соответствии с МСФО 9 с поддержкой принципа двойной записи, иерархией счетов и сторнируемых транзакций.

## 🛠 Стек

- Python 3.11+
- Django 4.2+
- SQLite
- Bootstrap 5 (для UI)

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/kao4uka/app-accounting.git
```
### 2. Установите и активируйте виртуальное окружение:
```bash
python -m venv venv
Linux: source venv/bin/activate 
Windows: venv\Scripts\activate
```
### 3. Установите зависимости:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 4. Загрузить тестовые данные и запустить сервер:
```bash 

python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

### 5. Открыть в браузере
```bash
http://127.0.0.1:8000/
