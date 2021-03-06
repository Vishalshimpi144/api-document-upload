"""added s3_document_name to document table

Revision ID: fe4f771caa28
Revises: 10d5b93b0023
Create Date: 2022-04-13 22:42:13.502283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe4f771caa28'
down_revision = '10d5b93b0023'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('s3_document_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 's3_document_name')
    # ### end Alembic commands ###
