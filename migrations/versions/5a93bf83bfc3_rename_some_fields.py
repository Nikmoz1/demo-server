"""rename some fields

Revision ID: 5a93bf83bfc3
Revises: dd20027f2272
Create Date: 2023-05-07 07:49:29.498530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a93bf83bfc3'
down_revision = 'dd20027f2272'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products') as batch_op:
        batch_op.alter_column('productNameTranslate', new_column_name='productNameRu')

    with op.batch_alter_table('products') as batch_op:
        batch_op.alter_column('descriptionTranslate', new_column_name='descriptionRu')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products') as batch_op:
        batch_op.alter_column('productNameRu', new_column_name='productNameTranslate')

    # Rename the 'productNameTranslate' column to 'positionNameRu'
    with op.batch_alter_table('products') as batch_op:
        batch_op.alter_column('descriptionRu', new_column_name='descriptionTranslate')

    # ### end Alembic commands ###