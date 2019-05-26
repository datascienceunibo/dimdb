import sqlite3
import os.path
from urllib.request import urlretrieve

import pandas as pd
from flask import current_app, g

from . import app

DB_URL = "https://bit.ly/2xFxVbt"
DB_FILENAME = "dimdb.db"

def db_path():
    return os.path.join(current_app.instance_path, DB_FILENAME)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(db_path())
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def download_db_file():
    urlretrieve(DB_URL, db_path())

def query(sql, *params):
    return pd.read_sql(sql, get_db(), params=params)

def query_one(sql, *params):
    results = query(sql, *params)
    if len(results) == 1:
        return results.iloc[0].to_dict()
    elif len(results) == 0:
        return None
    else:
        raise Exception("More than one row")

def get_movie(mid):
    return query_one("SELECT id, name, description, image_url FROM movie WHERE id=?", mid)

def get_movies(mids):
    return query("SELECT id, name FROM movie WHERE id in ({})".format(",".join("?" * len(mids))),
            *mids)

def get_all_movies():
    return query("SELECT * FROM movie ORDER BY id")

def get_random_movies(count):
    return query("""
        SELECT id, name, description, image_url
        FROM movie
        ORDER BY random()
        LIMIT ?
    """, count)

def get_movie_reviews(mid):
    return query("""
        SELECT p.id AS user_id, p.name AS user_name, r.stars, r.summary, r.review
        FROM review r
        JOIN person p ON r.person_id=p.id
        WHERE r.movie_id=?
        ORDER BY r.id
    """, mid)

def get_all_reviews():
    return query("SELECT review, stars FROM review ORDER BY id")

def get_user(uid):
    return query_one("SELECT id, name FROM person WHERE id=?", uid)

def get_user_reviews(uid):
    return query("""
        SELECT m.id AS movie_id, m.name AS movie_name, r.stars, r.summary, r.review
        FROM review r
        JOIN movie m ON r.movie_id=m.id
        WHERE r.person_id=?
        ORDER BY r.id
    """, uid)
