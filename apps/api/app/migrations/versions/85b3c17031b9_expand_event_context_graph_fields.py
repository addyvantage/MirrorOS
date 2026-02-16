"""expand event context graph fields

Revision ID: 85b3c17031b9
Revises: d73c9a82b7e9
Create Date: 2026-02-17 01:45:27.095902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85b3c17031b9'
down_revision: Union[str, Sequence[str], None] = 'd73c9a82b7e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "events",
        sa.Column("domain", sa.String(), nullable=False, server_default="unknown"),
    )
    op.add_column(
        "events",
        sa.Column("external_id", sa.String(), nullable=True),
    )
    op.add_column(
        "events",
        sa.Column("connector_id", sa.String(), nullable=False, server_default="legacy_import"),
    )
    op.add_column(
        "events",
        sa.Column(
            "ingestion_run_id",
            sa.Uuid(),
            nullable=False,
            server_default="00000000000000000000000000000000",
        ),
    )
    op.add_column(
        "events",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.add_column(
        "events",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_index("ix_events_external_id", "events", ["external_id"], unique=False)
    op.create_index("ix_events_connector_id", "events", ["connector_id"], unique=False)
    op.create_index("ix_events_domain", "events", ["domain"], unique=False)
    op.create_index("ix_events_ingestion_run_id", "events", ["ingestion_run_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_events_ingestion_run_id", table_name="events")
    op.drop_index("ix_events_domain", table_name="events")
    op.drop_index("ix_events_connector_id", table_name="events")
    op.drop_index("ix_events_external_id", table_name="events")

    with op.batch_alter_table("events") as batch_op:
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
        batch_op.drop_column("ingestion_run_id")
        batch_op.drop_column("connector_id")
        batch_op.drop_column("external_id")
        batch_op.drop_column("domain")
