from __future__ import annotations

from asyncio import run, sleep
from uuid import uuid4

import asyncpg
from dotenv import load_dotenv
from os import getenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, min_size=15, max_size=20,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')

    # actors

    async def get_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def get_actor(self, actor_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from actors where actor_id=$1', actor_id)
        return Actor(**dict(row)) if row else None

    async def upsert_actor(self, actor: Actor) -> Actor:
        if actor.actor_id is None:
            # insert; `actor` as no id assigned
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(name) VALUES ($1) returning *",
                                                actor.name)
        elif await self.get_actor(actor.actor_id) is None:
            # insert; `actor` has id assigned externally
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(actor_id,name) VALUES ($1,$2) returning *",
                                                actor.actor_id, actor.name)
        else:
            # update; `actor` with given id exists in db
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update actors set name=$2 where actor_id=$1 returning *""",
                                                actor.actor_id, actor.name)

        return Actor(**dict(row))

    async def get_movies(self, offset=0, limit=500) -> list[Movie]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movies order by title offset $1 limit $2', offset, limit)
        return [Movie(**dict(r)) for r in rows]

    async def get_movie(self, movie_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movies where movie_id=$1', movie_id)
        return Movie(**dict(row)) if row else None

    async def upsert_movie(self, movie: Movie) -> Movie:
        if movie.movie_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into movies(title,budget,popularity,release_date,revenue) 
                        VALUES ($1,$1,$2,$3,$4,$5) returning *""",
                    movie.title, movie.budget, movie.popularity, movie.release_date, movie.revenue)
        elif await self.get_movie(movie.movie_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into movies(movie_id,title,budget,popularity,release_date,revenue) 
                    VALUES ($1,$2,$3,$4,$5,$6) returning *""",
                    movie.movie_id, movie.title, movie.budget, movie.popularity, movie.release_date, movie.revenue)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movies set title=$2, budget = $3,
                                                popularity = $4,
                                                release_date = $5,
                                                revenue = $6 where movie_id=$1 returning *""",
                                                movie.movie_id, movie.title, movie.budget, movie.popularity,
                                                movie.release_date, movie.revenue)

        return Movie(**dict(row))

    async def get_movie_actor(self, movie_id: int, actor_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_actors where movie_id=$1 and actor_id=$2', movie_id,
                                            actor_id)
        return MovieActor(**dict(row)) if row else None

    async def get_movie_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movie_actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def upsert_movie_actor(self, movie_actor: MovieActor) -> MovieActor:
        if await self.get_movie_actor(movie_actor.movie_id, movie_actor.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into movie_actors(cast_id,movie_id,actor_id,credit_id,character,gender,position) 
                        VALUES ($1,$2, $3, $4, $5, $6, $7) returning *""",
                    movie_actor.cast_id, movie_actor.movie_id, movie_actor.actor_id, movie_actor.credit_id,
                    movie_actor.character, movie_actor.gender, movie_actor.position)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """update movie_actors set 
                        movie_id=$2, actor_id=$3, credit_id=$4, character=$5, gender=$6, position=$7  
                        where cast_id=$1 returning *""",
                    movie_actor.cast_id, movie_actor.movie_id, movie_actor.actor_id, movie_actor.credit_id,
                    movie_actor.character, movie_actor.gender, movie_actor.position)

        return MovieActor(**dict(row))
