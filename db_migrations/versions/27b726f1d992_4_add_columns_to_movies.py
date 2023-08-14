"""4_add_columns_to_movies

Revision ID: 27b726f1d992
Revises: bbf621ccd2b9
Create Date: 2023-08-10 16:53:58.985030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27b726f1d992'
down_revision = 'bbf621ccd2b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
     ALTER TABLE movies
        ADD COLUMN budget int,
        ADD COLUMN popularity float,
        ADD COLUMN release_date date,
        ADD COLUMN revenue int;
     """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE movies
        DROP COLUMN budget,
        DROP COLUMN popularity,
        DROP COLUMN release_date,
        DROP COLUMN revenue;
    """)
