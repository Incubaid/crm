"""empty message

Revision ID: bf2d7df5ad1f
Revises: 
Create Date: 2018-01-29 09:50:41.405904

"""
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'bf2d7df5ad1f'
down_revision = '6d2cafaad793'
branch_labels = None
depends_on = None

old_dealtype = postgresql.ENUM('HOSTER', 'ITO', 'PTO', 'AMBASSADOR', 'ITFT', 'PREPTO', name='dealtype')
new_dealtype = postgresql.ENUM('HOSTER', 'ITO', 'PTO', 'AMBASSADOR', 'ITFT', 'PREPTO', 'FARMER', name='dealtype')
temp_new_dealtype = postgresql.ENUM('HOSTER', 'ITO', 'PTO', 'AMBASSADOR', 'ITFT', 'PREPTO', 'FARMER', name='_dealtype')


def upgrade():
    temp_new_dealtype.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE deals ALTER COLUMN deal_type TYPE _dealtype'
               ' USING deal_type::text::_dealtype')

    old_dealtype.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    new_dealtype.create(op.get_bind(), checkfirst=False)

    op.execute('ALTER TABLE deals ALTER COLUMN deal_type TYPE dealtype'
               ' USING deal_type::text::dealtype')

    temp_new_dealtype.drop(op.get_bind(), checkfirst=False)


def downgrade():
    pass

