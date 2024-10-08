"""try to separate sec and ass

Revision ID: 84ec963825b1
Revises: e8667899cbf0
Create Date: 2024-08-06 18:21:13.223893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84ec963825b1'
down_revision: Union[str, None] = 'e8667899cbf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_product_association', schema=None) as batch_op:
        batch_op.drop_constraint('index_unique_orders_product', type_='unique')
        batch_op.create_unique_constraint('idx_unique_order_product', ['order_id', 'product_id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_product_association', schema=None) as batch_op:
        batch_op.drop_constraint('idx_unique_order_product', type_='unique')
        batch_op.create_unique_constraint('index_unique_orders_product', ['order_id', 'product_id'])

    # ### end Alembic commands ###
