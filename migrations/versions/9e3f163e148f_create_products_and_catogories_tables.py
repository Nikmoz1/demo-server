"""create products and catogories tables

Revision ID: 9e3f163e148f
Revises: 
Create Date: 2023-04-25 18:59:55.687433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e3f163e148f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('nameTranslate', sa.String(), nullable=True),
    sa.Column('parentId', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parentId'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('categoryId', sa.Integer(), nullable=True),
    sa.Column('productCode', sa.String(), nullable=False),
    sa.Column('positionNameUkr', sa.String(), nullable=False),
    sa.Column('positionNameRu', sa.String(), nullable=True),
    sa.Column('descriptionUkr', sa.String(), nullable=False),
    sa.Column('descriptionRu', sa.String(), nullable=True),
    sa.Column('priceInHryvnias', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('packageSize', sa.Float(), nullable=True),
    sa.Column('productSize', sa.Float(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('producer', sa.String(), nullable=True),
    sa.Column('producingCountry', sa.String(), nullable=True),
    sa.Column('dateCreatedProduct', sa.DateTime(timezone=True), nullable=False),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('discountPeriodTo', sa.Date(), nullable=True),
    sa.Column('discountPeriodFrom', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['categoryId'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productId', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['productId'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productId', sa.Integer(), nullable=False),
    sa.Column('video', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['productId'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_videos')
    op.drop_table('images')
    op.drop_table('products')
    op.drop_table('categories')
    # ### end Alembic commands ###