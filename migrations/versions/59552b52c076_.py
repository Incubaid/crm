"""empty message

Revision ID: 59552b52c076
Revises: 319951b3fda7
Create Date: 2018-02-04 03:08:37.309676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59552b52c076'
down_revision = '319951b3fda7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deals', sa.Column('owner_id', sa.String(length=5), nullable=True))
    op.drop_constraint('deals_referrer2_id_fkey', 'deals', type_='foreignkey')
    op.create_foreign_key(None, 'deals', 'users', ['owner_id'], ['id'])
    op.drop_column('deals', 'referrer2_id')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deals', sa.Column('referrer2_id', sa.VARCHAR(length=5), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'deals', type_='foreignkey')
    op.create_foreign_key('deals_referrer2_id_fkey', 'deals', 'contacts', ['referrer2_id'], ['id'])
    op.drop_column('deals', 'owner_id')
    # ### end Alembic commands ###