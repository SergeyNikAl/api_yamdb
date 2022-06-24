from reviews.models import Category, Comment, Genre, Review, Title, User
import csv
import os
import sqlite3

MAPPING = {
    'author': 'author_id',
    'id': 'pk',
    'category': 'category_id'
}

csv_folder_path = 'static/data/'

csv_models = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'review.csv': Review,
    'comments.csv': Comment,
}

path = 'db.sqlite3'
con = sqlite3.connect(path)
cur = con.cursor()
script_dir = os.path.join(os.path.dirname(
    __file__).replace('scripts', ''), 'static/data')


def save_model(row_dict, model):
    to_save = model(**row_dict)
    to_save.save()


def save_genre_title():
    with open(
        os.path.join(script_dir, 'genre_title.csv'),
        mode='r',
        encoding='utf-8'
    ) as fin:
        dr = csv.DictReader(fin)
        to_db = [(
            i['id'],
            i['title_id'],
            i['genre_id'],) for i in dr
        ]
    cur.executemany(
        "INSERT INTO reviews_title_genre"
        "(id, title_id, genre_id)"
        "VALUES (?, ?, ?);", to_db
    )
    con.commit()
    con.close()


def load_csv():
    for file_name, model in csv_models.items():
        with open(os.path.join(script_dir, file_name)) as file:
            reader = csv.reader(file)
            headline = next(reader)
            headline = [MAPPING.get(col, col) for col in headline]
            for row in reader:
                row_dict = {name: value for name, value in zip(headline, row)}
                save_model(row_dict, model)
    save_genre_title()
