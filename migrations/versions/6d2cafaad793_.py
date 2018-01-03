"""empty message

Revision ID: 6d2cafaad793
Revises: 7b948233c3ec
Create Date: 2018-01-02 15:09:51.139618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import random
import datetime
import string

# revision identifiers, used by Alembic.
revision = '6d2cafaad793'
down_revision = '7b948233c3ec'
branch_labels = None
depends_on = None

def migrate_mesages():
    tbl = sa.sql.table('messages',
                       sa.Column('id', sa.String(length=5), nullable=False),
                       sa.Column('author_original_id', sa.String),
                       sa.Column('author_original_type', sa.TIMESTAMP(), nullable=False))

    conn = op.get_bind()
    conn.execute("update messages set author_original_type='User'")


def migrate_emails():
    conn = op.get_bind()

    tbl = sa.sql.table('emails',
        sa.Column('id', sa.String(length=5), nullable=False),
        sa.Column('email', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('contact_id', sa.String),
        sa.Column('user_id', sa.String),
        sa.Column('company_id', sa.String),
        sa.Column('organization_id', sa.String),
    )

    data = []


    res = conn.execute("select id, emails from contacts").fetchall()
    emails = {}
    for result in res:
        for email in [e for e in result[1].split(',') if e]:

            emails[email] = emails.get(email, {})
            if 'contact_id' in emails[email]:
                print('duplicate contact email %s for %s & %s' % (email,  emails[email]['contact_id'], result[0]))
                continue
            emails[email]['contact_id'] = result[0]

    res = conn.execute("select id, emails from users").fetchall()

    for result in res:
        for email in [e for e in result[1].split(',') if e]:

            emails[email] = emails.get(email, {})
            if 'user_id' in emails[email]:
                print(
                'duplicate user email %s for %s, %s' % (emails[email], emails[email]['user_id'], result[0]))
            emails[email]['user_id'] = result[0]

    res = conn.execute("select id, emails from companies").fetchall()

    for result in res:
        for email in [e for e in result[1].split(',') if e]:
            emails[email] = emails.get(email, {})
            if 'company_id' in emails[email]:
                print(
                    'duplicate company email %s for %s, %s' % (emails[email], emails[email]['company_id'], result[0]))
                continue
            emails[email]['company_id'] = result[0]

    res = conn.execute("select id, emails from organizations").fetchall()

    for result in res:
        for email in [e for e in result[1].split(',') if e]:
            emails[email] = emails.get(email, {})
            if 'company_id' in emails[email]:
                print(
                    'duplicate organization email %s for %s, %s' % (emails[email], emails[email]['organization_id'], result[0]))
            emails[email]['organization_id'] = result[0]

    uids = set()

    while len(uids) != len(emails):
        uid = ''.join(random.sample(string.ascii_lowercase + string.digits, 5))
        uids.add(uid)

    uids = list(uids)

    for email, ids  in emails.items():
        d = {'email': email}
        d['id'] = uids.pop()
        d['contact_id'] = ids.get('contact_id')
        d['user_id'] = ids.get('user_id')
        d['company_id'] = ids.get('company_id')
        d['organization_id'] = ids.get('organiation_id')
        d['created_at'] =  datetime.datetime.now()
        d['updated_at'] = datetime.datetime.now()
        data.append(d)

    op.bulk_insert(tbl, data)


def migrate_phones():
    conn = op.get_bind()

    tbl = sa.sql.table('phones',
        sa.Column('id', sa.String(length=5), nullable=False),
        sa.Column('telephone', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('contact_id', sa.String),
        sa.Column('user_id', sa.String),
        sa.Column('company_id', sa.String),
    )

    data = []


    res = conn.execute("select id, telephones from contacts").fetchall()
    phones = {}
    for result in res:
        for phone in [e for e in result[1].split(',') if e]:

            phones[phone] = phones.get(phone, {})
            if 'contact_id' in phones[phone]:
                print('duplicate contact phone %s for %s & %s' % (phone,  phones[phone]['contact_id'], result[0]))
                continue
            phones[phone]['contact_id'] = result[0]

    res = conn.execute("select id, telephones from users").fetchall()

    for result in res:
        for phone in [e for e in result[1].split(',') if e]:

            phones[phone] = phones.get(phone, {})
            if 'user_id' in phones[phone]:
                print(
                'duplicate user phone %s for %s, %s' % (phones[phone], phones[phone]['user_id'], result[0]))
            phones[phone]['user_id'] = result[0]

    res = conn.execute("select id, telephones from companies").fetchall()

    for result in res:
        for phone in [e for e in result[1].split(',') if e]:
            phones[phone] = phones.get(phone, {})
            if 'company_id' in phones[phone]:
                print(
                    'duplicate company phone %s for %s, %s' % (phones[phone], phones[phone]['company_id'], result[0]))
                continue
            phones[phone]['company_id'] = result[0]

    uids = set()

    while len(uids) != len(phones):
        uid = ''.join(random.sample(string.ascii_lowercase + string.digits, 5))
        uids.add(uid)

    uids = list(uids)

    for phone, ids  in phones.items():
        d = {'telephone': phone}
        d['id'] = uids.pop()
        d['contact_id'] = ids.get('contact_id')
        d['user_id'] = ids.get('user_id')
        d['company_id'] = ids.get('company_id')
        d['created_at'] =  datetime.datetime.now()
        d['updated_at'] = datetime.datetime.now()
        data.append(d)

    op.bulk_insert(tbl, data)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emails',
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('id', sa.String(length=5), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('contact_id', sa.String(), nullable=True),
        sa.Column('organization_id', sa.String(), nullable=True),
        sa.Column('company_id', sa.String(), nullable=True),
        sa.Column('author_last_id', sa.String(length=5), nullable=True),
        sa.Column('author_original_id', sa.String(length=5), nullable=True),
        sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emails_email'), 'emails', ['email'], unique=True)

    migrate_emails()

    op.drop_index('ix_companies_emails', table_name='companies')
    op.drop_column('companies', 'emails')
    op.drop_index('ix_contacts_emails', table_name='contacts')
    op.drop_column('contacts', 'emails')


    op.add_column('links', sa.Column('filename', sa.String(), nullable=True))

    op.add_column('messages', sa.Column('author_original_type', sa.Unicode(length=255), nullable=True))
    op.add_column('messages', sa.Column('forced_destinations', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('parent_id', sa.String(length=5), nullable=True))
    op.alter_column('messages', 'content',
               existing_type=sa.TEXT(),
               nullable=False)

    op.drop_constraint('messages_author_original_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'messages', ['parent_id'], ['id'])
    op.drop_column('messages', 'time_tosend')
    op.drop_index('ix_organizations_emails', table_name='organizations')
    op.drop_column('organizations', 'emails')
    op.drop_index('ix_users_emails', table_name='users')
    op.drop_column('users', 'emails')

    migrate_mesages()

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phones',
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('id', sa.String(length=5), nullable=False),
                    sa.Column('telephone', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(), nullable=True),
                    sa.Column('contact_id', sa.String(), nullable=True),
                    sa.Column('company_id', sa.String(), nullable=True),
                    sa.Column('author_last_id', sa.String(length=5), nullable=True),
                    sa.Column('author_original_id', sa.String(length=5), nullable=True),
                    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
                    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_phones_telephone'), 'phones', ['telephone'], unique=True)

    migrate_phones()

    op.drop_index('ix_companies_telephones', table_name='companies')
    op.drop_column('companies', 'telephones')
    op.drop_index('ix_contacts_telephones', table_name='contacts')
    op.drop_column('contacts', 'telephones')
    op.drop_index('ix_users_telephones', table_name='users')
    op.drop_column('users', 'telephones')

    op.add_column('users', sa.Column('last_login', sa.TIMESTAMP(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('emails', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_users_emails', 'users', ['emails'], unique=False)
    op.add_column('organizations', sa.Column('emails', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_organizations_emails', 'organizations', ['emails'], unique=False)
    op.add_column('messages', sa.Column('time_tosend', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_author_original_id_fkey', 'messages', 'users', ['author_original_id'], ['id'])
    op.alter_column('messages', 'content',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_column('messages', 'parent_id')
    op.drop_column('messages', 'forced_destinations')
    op.drop_column('messages', 'author_original_type')
    op.drop_column('links', 'filename')
    op.add_column('contacts', sa.Column('emails', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_contacts_emails', 'contacts', ['emails'], unique=False)
    op.add_column('companies', sa.Column('emails', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_companies_emails', 'companies', ['emails'], unique=False)
    op.drop_index(op.f('ix_emails_email'), table_name='emails')
    op.drop_table('emails')
    # ### end Alembic commands ###

    op.add_column('users', sa.Column('telephones', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_users_telephones', 'users', ['telephones'], unique=False)
    op.add_column('contacts', sa.Column('telephones', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_contacts_telephones', 'contacts', ['telephones'], unique=False)
    op.add_column('companies', sa.Column('telephones', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_index('ix_companies_telephones', 'companies', ['telephones'], unique=False)
    op.drop_index(op.f('ix_phones_telephone'), table_name='phones')
    op.drop_table('phones')

    op.drop_column('users', 'last_login')