"""empty message

Revision ID: ed6e870e8ac1
Revises: 7564357e2e0b
Create Date: 2018-04-20 16:44:07.791474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed6e870e8ac1'
down_revision = '7564357e2e0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('uuid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('tag-relationship',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.uuid'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.uuid'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag-relationship')
    op.drop_table('tags')
    # ### end Alembic commands ###
