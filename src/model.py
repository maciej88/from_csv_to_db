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
