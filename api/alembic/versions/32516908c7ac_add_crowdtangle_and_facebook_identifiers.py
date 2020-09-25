"""Add crowdTangle and facebook identifiers

Revision ID: 32516908c7ac
Revises: 45455116256d
Create Date: 2020-09-11 15:58:32.101415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32516908c7ac'
down_revision = '45455116256d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('appearance',
                  sa.Column('crowdtangleIdentifier',
                            sa.String(32)))

    op.add_column('content',
                  sa.Column('crowdtangleIdentifier',
                            sa.String(32)))
    op.add_column('content',
                  sa.Column('facebookIdentifier',
                            sa.String(64)))

    op.add_column('medium',
                  sa.Column('crowdtangleIdentifier',
                            sa.String(32)))
    op.add_column('medium',
                  sa.Column('facebookIdentifier',
                            sa.String(64)))

def downgrade():
    sa.drop_column('appearance', 'crowdtangleIdentifier')

    sa.drop_column('content', 'crowdtangleIdentifier')
    sa.drop_column('content', 'facebookIdentifier')

    sa.drop_column('medium', 'crowdtangleIdentifier')
    sa.drop_column('medium', 'facebookIdentifier')
