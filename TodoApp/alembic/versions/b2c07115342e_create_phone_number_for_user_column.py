"""Create phone number for user column

Revision ID: b2c07115342e
Revises:
Create Date: 2026-08-28 17:33:32.587427

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2c07115342e"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone_number", sa.String(20), nullable=True))
    # pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone_number")
    # pass
