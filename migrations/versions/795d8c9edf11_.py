"""empty message

Revision ID: 795d8c9edf11
Revises: abcc14959b6c
Create Date: 2018-03-24 15:24:18.435900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '795d8c9edf11'
down_revision = 'abcc14959b6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('interests', sa.Text(), nullable=True))
    op.add_column('profile', sa.Column('location', sa.Text(), nullable=True))
    op.add_column('profile', sa.Column('meet', sa.Text(), nullable=True))
    op.add_column('profile', sa.Column('skills', sa.Text(), nullable=True))
    op.add_column('profile', sa.Column('work', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profile', 'work')
    op.drop_column('profile', 'skills')
    op.drop_column('profile', 'meet')
    op.drop_column('profile', 'location')
    op.drop_column('profile', 'interests')
    # ### end Alembic commands ###