"""empty message

Revision ID: 9d3a183554be
Revises: 
Create Date: 2017-03-13 20:59:44.271237

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9d3a183554be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('generalized_dialplan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dialplan', postgresql.JSON(), nullable=True),
    sa.Column('previous_version_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generalized_data_outgoing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generalized_dialplan_id', sa.Integer(), nullable=True),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('outgoing_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['generalized_dialplan_id'], ['generalized_dialplan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('outgoing_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=True),
    sa.Column('service', sa.String(length=100), nullable=True),
    sa.Column('call_start_time', sa.DateTime(), nullable=True),
    sa.Column('call_end_time', sa.DateTime(), nullable=True),
    sa.Column('call_duration', sa.Float(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=True),
    sa.Column('service_type', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('extension', sa.Integer(), nullable=True),
    sa.Column('isActive', sa.Boolean(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('allocated_channels', sa.Integer(), nullable=True),
    sa.Column('channels_inuse', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['generalized_dialplan.id'], ),
    sa.ForeignKeyConstraint(['service_type'], ['service_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('generalized_data_incoming',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generalized_dialplan_id', sa.Integer(), nullable=True),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('incoming_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['generalized_dialplan_id'], ['generalized_dialplan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('incoming_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_id', sa.Integer(), nullable=True),
    sa.Column('service', sa.String(length=100), nullable=True),
    sa.Column('call_start_time', sa.DateTime(), nullable=True),
    sa.Column('call_end_time', sa.DateTime(), nullable=True),
    sa.Column('call_duration', sa.Float(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['org_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('log_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['log_id'], ['incoming_log.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('incoming_log')
    op.drop_table('generalized_data_incoming')
    op.drop_table('service')
    op.drop_table('outgoing_log')
    op.drop_table('generalized_data_outgoing')
    op.drop_table('user')
    op.drop_table('service_type')
    op.drop_table('organization')
    op.drop_table('generalized_dialplan')
    # ### end Alembic commands ###
