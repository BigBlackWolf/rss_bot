"""Added resource

Revision ID: 4c782c3c5e3d
Revises: update_column_name
Create Date: 2021-12-23 23:47:16.543121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4c782c3c5e3d'
down_revision = '4c712c3c4ed21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(length=300), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_link'), 'resources', ['link'], unique=False)
    op.add_column('articles', sa.Column('resource_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'articles', 'resources', ['resource_id'], ['id'])
    op.alter_column('users', 'telegram_user_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'telegram_user_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'articles', type_='foreignkey')
    op.drop_column('articles', 'resource_id')
    op.drop_index(op.f('ix_resources_link'), table_name='resources')
    op.drop_table('resources')
    # ### end Alembic commands ###
