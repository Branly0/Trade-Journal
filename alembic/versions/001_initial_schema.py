"""Initial schema with all models

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing tables and enums first
    conn = op.get_bind()
    
    # Drop tables if they exist (in reverse dependency order)
    tables = ['trade_screenshots', 'trade_notes', 'trades', 'users', 'symbols']
    for table in tables:
        conn.execute(sa.text(f"DROP TABLE IF EXISTS {table} CASCADE"))
    
    # Drop enums if they exist
    enum_types = ['assettypeenum', 'currencyenum', 'usertypeenum', 'sessionenum', 'strategyenum']
    for enum_type in enum_types:
        conn.execute(sa.text(f"DROP TYPE IF EXISTS {enum_type} CASCADE"))
    
    # Create symbols table
    op.create_table('symbols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('asset_type', sa.Enum('forex', 'stocks', 'crypto', 'indexes', name='assettypeenum'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('pip_size', sa.Float(), nullable=False),
    sa.Column('tick_size', sa.Float(), nullable=False),
    sa.Column('quote_currency', sa.Enum('USD', 'EUR', 'GBP', 'JPY', name='currencyenum'), nullable=True),
    sa.Column('base_currency', sa.Enum('USD', 'EUR', 'GBP', 'JPY', name='currencyenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_symbols_id'), 'symbols', ['id'], unique=False)
    
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('user_type', sa.Enum('admin', 'trader', name='usertypeenum'), nullable=False),
    sa.Column('profile_picture_url', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    
    # Create trades table
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('max_duration_min', sa.Integer(), nullable=True),
    sa.Column('entry', sa.Float(), nullable=False),
    sa.Column('exit', sa.Float(), nullable=False),
    sa.Column('stop_loss', sa.Float(), nullable=False),
    sa.Column('take_profit', sa.Float(), nullable=False),
    sa.Column('is_closed', sa.Boolean(), nullable=False, server_default='false'),
    sa.Column('time_frame', sa.Integer(), nullable=False),
    sa.Column('session', sa.Enum('London', 'New_York', 'Asia', name='sessionenum'), nullable=False),
    sa.Column('strategy', sa.Enum('scalping', 'day_trading', 'swing_trading', 'position_trading', name='strategyenum'), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trades_id'), 'trades', ['id'], unique=False)
    
    # Create trade_notes table
    op.create_table('trade_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(), nullable=False),
    sa.Column('trade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trade_notes_id'), 'trade_notes', ['id'], unique=False)
    
    # Create trade_screenshots table
    op.create_table('trade_screenshots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('screenshot_url', sa.String(), nullable=False),
    sa.Column('trade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trade_screenshots_id'), 'trade_screenshots', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_trade_screenshots_id'), table_name='trade_screenshots', if_exists=True)
    op.drop_table('trade_screenshots', if_exists=True)
    op.drop_index(op.f('ix_trade_notes_id'), table_name='trade_notes', if_exists=True)
    op.drop_table('trade_notes', if_exists=True)
    op.drop_index(op.f('ix_trades_id'), table_name='trades', if_exists=True)
    op.drop_table('trades', if_exists=True)
    op.drop_index(op.f('ix_symbols_id'), table_name='symbols', if_exists=True)
    op.drop_table('symbols', if_exists=True)
    op.drop_index(op.f('ix_users_id'), table_name='users', if_exists=True)
    op.drop_table('users', if_exists=True)
