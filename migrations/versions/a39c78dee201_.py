"""empty message

Revision ID: a39c78dee201
Revises: 8cd77829df26
Create Date: 2018-07-18 15:27:57.794214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a39c78dee201'
down_revision = '8cd77829df26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('url', sa.String(length=150), nullable=True),
    sa.Column('date', sa.String(length=150), nullable=True),
    sa.Column('format', sa.String(length=150), nullable=True),
    sa.Column('season', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
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
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], ),
    sa.PrimaryKeyConstraint('deck_id', 'card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deck_cards')
    op.drop_table('deck')
    op.drop_table('events')
    # ### end Alembic commands ###
