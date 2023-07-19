from dataclasses import dataclass

"""
Models to serialize data for import tools and serialize data.
"""


@dataclass
class Movie:
    movie_id: int
    title: str


@dataclass
class Actor:
    actor_id: int
    name: str


@dataclass
class MovieActor:
    cast_id: int
    movie_id: int
    actor_id: int
    credit_id: str
    character: str
    gender: int
    order_: int


@dataclass(frozen=True)
class CastEntry:
    movie_index: int  # dodane... rząd w csv-ie
    cast_id: int
    character: str
    credit_id: str
    gender: int
    id: int  # id of ... the actor?
    name: str
    order: int
