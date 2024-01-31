"""URL red social

Revision ID: 33ce9933ce1f
Revises: 038b625a6883
Create Date: 2024-01-08 06:08:16.905137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33ce9933ce1f'
down_revision = '038b625a6883'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_social_networks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_social_networks', schema=None) as batch_op:
        batch_op.drop_column('url')

    # ### end Alembic commands ###