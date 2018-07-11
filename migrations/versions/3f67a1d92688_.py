"""empty message

Revision ID: 3f67a1d92688
Revises: c0f9f2132e2f
Create Date: 2018-07-19 13:50:02.004201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f67a1d92688'
down_revision = 'c0f9f2132e2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('deck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deck_cards',
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('main_count', sa.Integer(), nullable=True),
    sa.Column('sideboard_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.PrimaryKeyConstraint('deck_id', 'card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deck_cards')
    op.drop_table('deck')
    op.drop_table('card')
    # ### end Alembic commands ###
