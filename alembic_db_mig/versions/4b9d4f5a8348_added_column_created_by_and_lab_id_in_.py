"""added column created_by and lab id in user allowed to be null

Revision ID: 4b9d4f5a8348
Revises: 25b8f76586d6
Create Date: 2022-04-03 17:17:47.868977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b9d4f5a8348'
down_revision = '25b8f76586d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'lab', 'users', ['created_by'], ['id'], ondelete='SET DEFAULT')
    op.alter_column('users', 'lab_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'lab_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'lab', type_='foreignkey')
    # ### end Alembic commands ###
