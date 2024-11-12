"""Initial revision

Revision ID: 459a2acd2cd0
Revises: 
Create Date: 2024-11-06 14:09:55.529144

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = '459a2acd2cd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('last_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('age', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='my_app_schema'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customers', schema='my_app_schema')
    # ### end Alembic commands ###