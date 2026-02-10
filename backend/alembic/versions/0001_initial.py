"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-07
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('phone', sa.String(length=30), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='USER'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('account_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('account_type', sa.String(length=50), nullable=False, server_default='SAVINGS'),
        sa.Column('balance', sa.Numeric(12,2), nullable=False, server_default='0'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'),
    )

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('from_account', sa.String(length=50), nullable=True),
        sa.Column('to_account', sa.String(length=50), nullable=True),
        sa.Column('amount', sa.Numeric(12,2), nullable=False),
        sa.Column('transaction_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='COMPLETED'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('transactions')
    op.drop_table('accounts')
    op.drop_table('users')
