import json
from collections.abc import Collection

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
