"""add phone number

Revision ID: 2ace795638bd
Revises: 
Create Date: 2021-11-01 09:56:00.275588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2ace795638bd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user", sa.Column("phone_number", sa.String(), nullable=True)
    )
    pass


def downgrade():
    op.drop_column("user", "phone_number")
    pass
