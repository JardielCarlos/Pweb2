"""adicionando empresa ao cardapio

Revision ID: 5b20962f81ff
Revises: f31323ad3731
Create Date: 2023-06-09 11:36:47.000707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b20962f81ff'
down_revision = 'f31323ad3731'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_fichatecnicaoperacional')
    with op.batch_alter_table('tb_cardapio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('empresa_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'tb_empresa', ['empresa_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_cardapio', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('empresa_id')

    op.create_table('tb_fichatecnicaoperacional',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tb_fichatecnicaoperacional_pkey')
    )
    # ### end Alembic commands ###
