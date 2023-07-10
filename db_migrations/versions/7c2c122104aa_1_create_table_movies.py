"""1_create_table_movies

Revision ID: 7c2c122104aa
Revises: 
Create Date: 2023-07-09 17:44:15.063772

"""
import os

from alembic import op
from dotenv import load_dotenv
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c2c122104aa'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    create table movies(
        movie_id serial primary key,
        title text
    );
    """)


def downgrade() -> None:
    op.execute("""
    drop table movies;
    """)
