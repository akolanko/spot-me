"""empty message

Revision ID: b6b121b88482
Revises: 0400ec0a51ad
Create Date: 2018-03-24 14:55:09.308757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6b121b88482'
down_revision = '0400ec0a51ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('work', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profile', 'work')
    # ### end Alembic commands ###
