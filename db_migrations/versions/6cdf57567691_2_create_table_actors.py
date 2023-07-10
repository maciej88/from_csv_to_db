"""2_create_table_actors

Revision ID: 6cdf57567691
Revises: 7c2c122104aa
Create Date: 2023-07-10 18:23:28.072049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cdf57567691'
down_revision = '7c2c122104aa'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute("""
    create table actors(
       actor_id serial primary key,
       name text not null
    )
    """)

def downgrade() -> None:
    op.execute("""
    drop table actors;
    """)

