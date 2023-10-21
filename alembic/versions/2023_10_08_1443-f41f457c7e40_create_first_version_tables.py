"""create first version tables

Revision ID: f41f457c7e40
Revises: 
Create Date: 2023-10-08 14:43:10.670146

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f41f457c7e40'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("statuses",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(150), nullable=False),
                    sa.Column('description', sa.String(255), nullable=True),
                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )
    op.create_table("users",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('status_id', sa.Integer, sa.ForeignKey("statuses.id")),
                    sa.Column('name', sa.String(150), nullable=False),
                    sa.Column('email', sa.String(255), nullable=False),
                    sa.Column('remember_token', sa.String(255), nullable=True),
                    sa.Column('hashed_password', sa.String(255), nullable=False),
                    sa.Column('email_verified_at', sa.DateTime, nullable=True),
                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )
    op.create_table("companies",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id")),

                    sa.Column('name', sa.String(150), nullable=False),
                    sa.Column('registration_number', sa.String(100), nullable=False),
                    sa.Column('main_contact_number', sa.String(255), nullable=False),
                    sa.Column('secondary_contact_number', sa.String(255), nullable=True),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )

    op.create_table("addresses",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('company_id', sa.Integer, sa.ForeignKey("companies.id")),

                    sa.Column('street_name', sa.String(255)),
                    sa.Column('street_number', sa.String(10)),
                    sa.Column('suburb', sa.String(150)),
                    sa.Column('city', sa.String(150)),
                    sa.Column('province_state', sa.String(255)),
                    sa.Column('postal_zip_code', sa.String(20)),
                    sa.Column('country', sa.String(150)),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )

    op.create_table("abilities",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('status_id', sa.Integer, sa.ForeignKey("statuses.id")),

                    sa.Column('name', sa.String(150)),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )

    op.create_table("applications",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('status_id', sa.Integer, sa.ForeignKey("statuses.id")),
                    sa.Column('company_id', sa.Integer, sa.ForeignKey("companies.id")),

                    sa.Column('name', sa.String(150)),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )

    op.create_table("access_tokens",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('application_id', sa.Integer, sa.ForeignKey("applications.id")),

                    sa.Column('token', sa.String),
                    sa.Column('last_used_at', sa.DateTime, nullable=True),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )

    op.create_table("datasets",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('status_id', sa.Integer, sa.ForeignKey("statuses.id")),

                    sa.Column('name', sa.String),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )

    op.create_table("dataset_items",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('dataset_id', sa.Integer, sa.ForeignKey("datasets.id")),
                    sa.Column('access_token_id', sa.Integer, sa.ForeignKey("access_tokens.id")),
                    sa.Column('status_id', sa.Integer, sa.ForeignKey("statuses.id")),

                    sa.Column('type', sa.String),
                    sa.Column('file_path', sa.String),
                    sa.Column('file_metadata', sa.String),

                    sa.Column('created_at', sa.DateTime, server_default=str(datetime.now())),
                    sa.Column('updated_at', sa.DateTime, server_default=str(datetime.now())),
                    )


def downgrade() -> None:
    op.drop_table("dataset_items")
    op.drop_table("datasets")
    op.drop_table("access_tokens")
    op.drop_table("applications")
    op.drop_table("abilities")
    op.drop_table("addresses")
    op.drop_table("companies")
    op.drop_table("users")
    op.drop_table("statuses")
