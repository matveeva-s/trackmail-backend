"""empty message

Revision ID: 533f49a7a57f
Revises: 
Create Date: 2019-05-06 19:56:24.529118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '533f49a7a57f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('is_group_chat', sa.Boolean(), nullable=False),
    sa.Column('topic', sa.String(), nullable=True),
    sa.Column('last_message', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('chat_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=False),
    sa.Column('last_name', sa.String(length=40), nullable=False),
    sa.Column('nick', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('is_auth', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nick')
    )
    op.create_table('member',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.chat_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'chat_id')
    )
    op.create_table('message',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.chat_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('message_id')
    )
    op.create_table('attachment',
    sa.Column('attachment_id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('url', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.chat_id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['message.message_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('attachment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attachment')
    op.drop_table('message')
    op.drop_table('member')
    op.drop_table('user')
    op.drop_table('chat')
    # ### end Alembic commands ###
