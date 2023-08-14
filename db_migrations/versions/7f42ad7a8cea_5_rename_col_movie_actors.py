"""5_rename_col_movie_actors

Revision ID: 7f42ad7a8cea
Revises: 27b726f1d992
Create Date: 2023-08-14 16:20:20.830537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f42ad7a8cea'
down_revision = '27b726f1d992'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
     ALTER TABLE movie_actors
        RENAME COLUMN order_ TO position;
     """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE movie_actors
        RENAME COLUMN position TO order_;
    """)
