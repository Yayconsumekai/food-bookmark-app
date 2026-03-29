"""add total_minutes column to recipes

Revision ID: 6169b2e20401
Revises: 790eeecb461c
Create Date: 2026-03-29 00:28:12.612908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6169b2e20401'
down_revision: Union[str, Sequence[str], None] = '790eeecb461c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('recipes', sa.Column('total_minutes', sa.Integer(), nullable=True))

    # Populate it by parsing the existing total_time string
    op.execute("""
        UPDATE recipes SET total_minutes = (
            COALESCE(
                CASE 
                    WHEN total_time ~ '(\d+)\s*h'
                    THEN (regexp_match(total_time, '(\d+)\s*h'))[1]::int * 60
                    ELSE 0
                END
            ) +
            COALESCE(
                CASE 
                    WHEN total_time ~ '(\d+)\s*m'
                    THEN (regexp_match(total_time, '(\d+)\s*m'))[1]::int
                    ELSE 0
                END
            )
        )
        WHERE total_time IS NOT NULL
    """)

    op.create_index('idx_recipes_total_minutes', 'recipes', ['total_minutes'])

def downgrade():
    op.drop_index('idx_recipes_total_minutes')
    op.drop_column('recipes', 'total_minutes')
