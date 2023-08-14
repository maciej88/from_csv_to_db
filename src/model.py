from dataclasses import dataclass
from datetime import date

"""
Models to serialize data for import tools and serialize data.
"""


@dataclass
class Movie:
    movie_id: int
    title: str
    budget: int
    popularity: float
    release_date: date
    revenue: int


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
    position: int


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


@dataclass
class Crew:
    credit_id: str  # unique
    movie_id: int   # credit_id → (single, unique) movie_id ---> *:1 relation (no need for join-table)
    department: str
    gender: int
    id: int  # id of ... the person?
    job: str
    name: str
