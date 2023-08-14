import json
from collections.abc import Collection
from datetime import datetime

import pandas as pd

from model import *

pd.options.display.max_rows = 10


def get_actors(filename: str) -> Collection[Actor]:
    casts = get_casts(filename)
    actors = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        actors.extend([(c.id, c.name) for c in entries])
    actors = set(actors)
    return [Actor(*a) for a in actors]


def get_casts(filename: str) -> list[str]:
    df_ = pd.read_csv(filename)
    return list(df_['cast'])


def get_cast_of_movie(index: int, cast_field: str) -> list[CastEntry]:
    dicts = json.loads(cast_field)
    entries = []
    for d in dicts:
        entry = CastEntry(movie_index=index, **d)
        entries.append(entry)
    return entries


def get_movies(filename: str) -> Collection[Movie]:
    df_ = pd.read_csv(filename)
    df_sub = df_.loc[:, ['id', 'title', 'budget', 'popularity', 'release_date', 'revenue']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    movies = []
    for d in df_as_dict:
        rdate = d['release_date']
        try:
            release_date = datetime.strptime(str(rdate), '%Y-%m-%d').date()
        except ValueError as e:
            print(rdate)
            continue
        m = Movie(movie_id=d['id'], title=d['title'], budget=d['budget'], popularity=d['popularity'],
                  release_date=release_date, revenue=d['revenue'] / 1000)
        movies.append(m)
    return movies

def get_movie_actors(filename: str) -> Collection[MovieActor]:
    df_ = pd.read_csv(filename)
    df_sub = df_.loc[:, ['movie_id', 'cast']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')

    res = []
    for row in df_as_dict:
        movie_id = row['movie_id']
        cast_as_str = row['cast']
        entries: list[CastEntry] = get_cast_of_movie(movie_id, cast_as_str)

        movie_actors = [to_movie_actor(c) for c in entries]
        res.extend(movie_actors)

    return res

def to_movie_actor(cast_entry: CastEntry) -> MovieActor:
    c = cast_entry
    return MovieActor(movie_id=c.movie_index, actor_id=c.id, cast_id=c.cast_id, credit_id=c.credit_id,
                      character=c.character, gender=c.gender, position=c.order)
