# Проект "YaMDb"
Проект "YaMDb" позволяет собирать отзывы пользователей на книги, фильмы, музыку.

### Авторы:
- [Sergey Nikulin] (https://github.com/SergeyNikAl)
- [Tatayna] (https://github.com/belkalev)
- [Alibek Ubaidullayev] (https://github.com/alibekubaidullayev)

### Технологии:
- Python
- Django
- DRF
- SQLite3

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeyNikAl/api_yamdb.git
```

```
cd api_yambd
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
### Как запустить тестовое наполнение базы:
Установочный файл тестовой базы находится по адресу
```
../api_yamdb/api_yamdb/scripts/load_csv.py
```
Запустить оболочку Django shell
```
python3 manage.py shell
```
Ввести следующий код
```
from scripts.load_csv import load_csv
load_csv()
```