"""init

Revision ID: 611014881d99
Revises: 
Create Date: 2024-01-16 13:28:37.833009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '611014881d99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contract_address', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('symbol', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('multitokencollections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contract_address', sa.Integer(), nullable=True),
    sa.Column('uri', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('multitokenholders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('account', sa.Text(), nullable=True),
    sa.Column('token_id', sa.Integer(), nullable=True),
    sa.Column('hash', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['multitokencollections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('multitokenholders')
    op.drop_table('multitokencollections')
    op.drop_table('collections')
    # ### end Alembic commands ###
