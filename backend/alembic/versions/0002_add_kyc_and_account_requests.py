"""add_kyc_and_account_requests

Revision ID: 0002
Revises: 0001_initial
Create Date: 2026-02-11
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # add user fields if missing
    if 'users' in inspector.get_table_names():
        existing = [c['name'] for c in inspector.get_columns('users')]
        if 'address' not in existing:
            op.add_column('users', sa.Column('address', sa.String(length=500), nullable=True))
        if 'dob' not in existing:
            op.add_column('users', sa.Column('dob', sa.String(length=50), nullable=True))
        if 'government_id' not in existing:
            op.add_column('users', sa.Column('government_id', sa.String(length=100), nullable=True))
        if 'kyc_status' not in existing:
            op.add_column('users', sa.Column('kyc_status', sa.String(length=50), nullable=False, server_default='PENDING'))

    # add account fields if missing
    if 'accounts' in inspector.get_table_names():
        existing = [c['name'] for c in inspector.get_columns('accounts')]
        if 'branch' not in existing:
            op.add_column('accounts', sa.Column('branch', sa.String(length=150), nullable=True))
        if 'ifsc' not in existing:
            op.add_column('accounts', sa.Column('ifsc', sa.String(length=50), nullable=True))
        if 'created_at' not in existing:
            op.add_column('accounts', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')))

    # create account_requests table only if it does not exist
    if 'account_requests' not in inspector.get_table_names():
        op.create_table(
            'account_requests',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('account_type', sa.String(length=50), nullable=False),
            sa.Column('branch', sa.String(length=150), nullable=True),
            sa.Column('initial_deposit', sa.Numeric(12,2), nullable=False, server_default='0'),
            sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING_APPROVAL'),
            sa.Column('reason', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        )


def downgrade():
    op.drop_table('account_requests')
    op.drop_column('accounts', 'created_at')
    op.drop_column('accounts', 'ifsc')
    op.drop_column('accounts', 'branch')
    op.drop_column('users', 'kyc_status')
    op.drop_column('users', 'government_id')
    op.drop_column('users', 'dob')
    op.drop_column('users', 'address')
