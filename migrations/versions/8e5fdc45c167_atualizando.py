"""atualizando

Revision ID: 8e5fdc45c167
Revises: 
Create Date: 2023-06-19 09:30:51.598676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e5fdc45c167'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_cardapio', schema=None) as batch_op:
        batch_op.drop_column('nome')

    with op.batch_alter_table('tb_modopreparo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_modopreparo', schema=None) as batch_op:
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('tb_cardapio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome', sa.VARCHAR(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###