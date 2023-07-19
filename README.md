# from_csv_to_db

Project made for simple demonstrate possibility of use:
- PostgreSQL database - relational database,
- Alembic: to make migrations (create or drop table),
- asynchronous functions: to efficiently import data from csv file to database,

Project setup:
Environment for project is from poetry - all packages in poetry.lock.
Please specify database url (sqlalchemy) and schema name in ".env" file.

Source file for data import (kaggle.com):
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv