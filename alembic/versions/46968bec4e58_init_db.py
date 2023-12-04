"""init db

Revision ID: 46968bec4e58
Revises: 
Create Date: 2023-12-03 23:40:23.699840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '46968bec4e58'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('password', sa.VARCHAR(length=50), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=50), nullable=False),
    sa.Column('balance', sa.NUMERIC(precision=10, scale=2), server_default='0.00', nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("date_trunc('s', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('transaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.Column('amount', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.Column('message', sa.TEXT(), nullable=True),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("date_trunc('s', now())"), nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_amount'), 'transaction', ['amount'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_amount'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_table('user')
    # ### end Alembic commands ###