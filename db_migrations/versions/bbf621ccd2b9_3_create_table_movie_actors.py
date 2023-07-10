"""3_create_table_movie_actors

Revision ID: bbf621ccd2b9
Revises: 6cdf57567691
Create Date: 2023-07-10 18:25:44.660183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbf621ccd2b9'
down_revision = '6cdf57567691'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
     create table movie_actors(
        movie_id int references movies(movie_id) on DELETE cascade,
        actor_id int references actors(actor_id) on DELETE cascade,
        cast_id int,
        character text,
        credit_id text,
        gender int,
        order_ int
     );
     """)


def downgrade() -> None:
    op.execute("""
    drop table movie_actors;
    """)
