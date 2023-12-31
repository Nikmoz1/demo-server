"""updating the productNameUkr field to nullable

Revision ID: e8caf8779076
Revises: 947929f9e58a
Create Date: 2023-05-15 16:14:04.463527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8caf8779076'
down_revision = '947929f9e58a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('productNameUkr',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('productNameUkr',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
