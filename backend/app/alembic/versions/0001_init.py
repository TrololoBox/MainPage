"""initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('role', sa.Enum('admin', 'teacher', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'students',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('student_class', sa.String, nullable=False),
        sa.Column('parent_email', sa.String),
        sa.Column('parent_phone', sa.String),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'excursions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('student_class', sa.String, nullable=False),
        sa.Column('date', sa.String, nullable=False),
        sa.Column('location', sa.String, nullable=False),
        sa.Column('price', sa.Integer),
        sa.Column('description', sa.Text),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'signatures',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('excursion_id', sa.Integer, sa.ForeignKey('excursions.id'), nullable=False),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('students.id'), nullable=False),
        sa.Column('mode', sa.Enum('vector', 'pdf', name='signaturemode'), nullable=False),
        sa.Column('strokes', sa.JSON),
        sa.Column('pdf_path', sa.String),
        sa.Column('metadata_json', sa.JSON),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'reminders',
        sa.Column('log_id', sa.Integer, primary_key=True),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('students.id'), nullable=False),
        sa.Column('excursion_id', sa.Integer, sa.ForeignKey('excursions.id'), nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now()),
        sa.Column('result', sa.String),
    )


def downgrade():
    op.drop_table('reminders')
    op.drop_table('signatures')
    op.drop_table('excursions')
    op.drop_table('students')
    op.drop_table('users')
