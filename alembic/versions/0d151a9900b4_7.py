"""7

Revision ID: 0d151a9900b4
Revises: 3068d213a5af
Create Date: 2022-02-09 20:00:44.758629

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0d151a9900b4'
down_revision = '3068d213a5af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.add_column('auth_user', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.add_column('auth_user', sa.Column('last_name', sa.String(length=50), nullable=True))
    op.add_column('auth_user', sa.Column('other_name', sa.String(length=50), nullable=True))
    op.add_column('auth_user', sa.Column('email', sa.String(length=50), nullable=True))
    op.add_column('auth_user', sa.Column('phone', sa.String(length=12), nullable=True))
    op.add_column('auth_user', sa.Column('birthday', sa.DateTime(timezone=True), nullable=True))
    op.add_column('auth_user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auth_user', 'is_admin')
    op.drop_column('auth_user', 'birthday')
    op.drop_column('auth_user', 'phone')
    op.drop_column('auth_user', 'email')
    op.drop_column('auth_user', 'other_name')
    op.drop_column('auth_user', 'last_name')
    op.drop_column('auth_user', 'first_name')
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('other_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=12), autoincrement=False, nullable=True),
    sa.Column('birthday', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    # ### end Alembic commands ###