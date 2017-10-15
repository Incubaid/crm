"""empty message
Revision ID: 079e82e64d60
Revises: 7510ff711e3d
Create Date: 2017-10-15 16:22:14.944094
"""
import random
import string
import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '079e82e64d60'
down_revision = '7510ff711e3d'
branch_labels = None
depends_on = None

COUNTRIES = postgresql.ENUM('Czech Republic', 'Nepal', 'Switzerland', 'Papua New Guinea', 'Australia', 'Kyrgyzstan', 'Antigua and Barbuda', 'Qatar', 'Pakistan', 'Ecuador', 'Palau', 'Mongolia', 'Comoros', 'Nauru', 'Belgium', 'Portugal', 'Sweden', 'Liberia', 'Kuwait', 'Brazil', 'Canada', 'Angola', 'Trinidad and Tobago', 'Cape Verde', 'Mauritius', 'Samoa', 'Ethiopia', 'Saint Vincent and the Grenadines', 'Anguilla', 'Senegal', 'Reunion', 'Morocco', 'Costa Rica', 'French Southern Territories', "Korea, Democratic People's Republic of", 'Tuvalu', 'Saint Kitts and Nevis', 'Guyana', 'Bangladesh', 'Tokelau', 'Afghanistan', 'Egypt', 'Peru', 'Moldova, Republic of', 'Rwanda', 'British Indian Ocean Territory', 'Albania', 'Philippines', 'Serbia and Montenegro', 'Lithuania', 'Mayotte', 'Saint Helena', 'Mexico', 'Timor-Leste', 'Central African Republic', 'Equatorial Guinea', 'Saudi Arabia', 'Bahamas', 'Tunisia', 'Kenya', 'United States', 'South Georgia and the South Sandwich Islands', 'Panama', 'Poland', 'Puerto Rico', 'Macedonia, the Former Yugoslav Republic of', 'Jamaica', 'Bolivia', 'Croatia', 'Virgin Islands, British', 'Chad', 'Marshall Islands', 'Italy', 'Monaco', 'Norfolk Island', 'Taiwan, Province of China', 'Grenada', 'Haiti', 'Slovenia', 'Zimbabwe', 'Namibia', 'Holy See (Vatican City State)', 'Malawi', 'Macao', 'Zambia', 'Faroe Islands', 'Vanuatu', 'Iceland', 'Iraq', 'Uruguay', 'New Caledonia', 'New Zealand', 'Kazakhstan', 'Togo', 'United Arab Emirates', 'French Polynesia', 'Netherlands Antilles', 'Armenia', 'Maldives', 'Denmark', 'Honduras', 'Lebanon', 'Cambodia', 'Chile', 'Cyprus', 'Tajikistan', 'Latvia', 'Jordan', 'Niue', 'Fiji', 'Northern Mariana Islands', 'Ireland', 'Guadeloupe', 'Cocos (Keeling) Islands', 'Yemen', 'Svalbard and Jan Mayen', 'French Guiana', 'Turkey', 'Sierra Leone', 'Germany', 'Syrian Arab Republic', 'Libyan Arab Jamahiriya', 'Gabon', 'Antarctica', 'Dominica', 'Ukraine', 'Korea, Republic of', 'Niger', 'Martinique', 'Nigeria', 'Virgin Islands, U.s.', 'Dominican Republic', 'Pitcairn', 'Malta', 'Turks and Caicos Islands', 'Viet Nam', 'Burundi', 'Swaziland', 'Argentina', "Lao People's Democratic Republic", 'Malaysia', 'Solomon Islands', 'Venezuela', 'Andorra', 'Christmas Island', 'Botswana', 'Mauritania', 'Myanmar', 'United States Minor Outlying Islands', 'Bulgaria', 'Bahrain', 'Lesotho', "Cote D'Ivoire", 'Congo', 'Belize', 'Bosnia and Herzegovina', 'Sudan', 'Spain', 'Iran, Islamic Republic of', 'Barbados', 'Somalia', 'Netherlands', 'Gibraltar', 'United Kingdom', 'Bermuda', 'Kiribati', 'Brunei Darussalam', 'Saint Lucia', 'Heard Island and Mcdonald Islands', 'South Africa', 'Palestinian Territory, Occupied', 'Austria', 'Greece', 'Mali', 'Singapore', 'France', 'Falkland Islands (Malvinas)', 'Romania', 'Finland', 'Cuba', 'Georgia', 'Guinea-Bissau', 'Bouvet Island', 'Uzbekistan', 'Hong Kong', 'Wallis and Futuna', 'Gambia', 'American Samoa', 'Aruba', 'Cook Islands', 'Israel', 'Cayman Islands', 'Estonia', 'Uganda', 'Madagascar', 'Greenland', 'Djibouti', 'Belarus', 'Liechtenstein', 'Tonga', 'San Marino', 'Sao Tome and Principe', 'Azerbaijan', 'Suriname', 'Ghana', 'Benin', 'Western Sahara', 'Bhutan', 'Guam', 'Seychelles', 'Nicaragua', 'Japan', 'Guinea', 'Cameroon', 'Saint Pierre and Miquelon', 'Slovakia', 'Micronesia, Federated States of', 'Montserrat', 'Algeria', 'Oman', 'Eritrea', 'Burkina Faso', 'Indonesia', 'Colombia', 'Norway', 'Congo, the Democratic Republic of the', 'China', 'Thailand', 'Russian Federation', 'Hungary', 'Guatemala', 'India', 'Turkmenistan', 'Paraguay', 'El Salvador', 'Tanzania, United Republic of', 'Sri Lanka', 'Mozambique', 'Luxembourg', name='countries', create_type=False)


def get_contact_old_addresses():
    address_table = sa.sql.table('addresses',
        sa.Column('id', sa.String(length=5), nullable=False),
         sa.Column('contact_id', sa.String(length=5), nullable=False),
        sa.Column('country', sa.String),
        sa.Column('zip_code', sa.String),
        sa.Column('street_number', sa.String),
        sa.Column('street_name', sa.String),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    )

    conn = op.get_bind()

    res = conn.execute(
        "select id,country,zip_code,street_number,street_name from contacts"
    )

    db_results = res.fetchall()

    uids = set()

    while len(uids) != len(db_results):
        uid = ''.join(random.sample(string.ascii_lowercase + string.digits,5))
        uids.add(uid)

    uids = list(uids)

    data = []
    for result in db_results:
        data.append({
            'id': uids.pop(),
            'contact_id': result[0],
            'country': result[1],
            'zip_code': result[2],
            'street_number': result[3],
            'street_name': result[4],
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })

    return address_table, data


def add_contact_subgroups():
    subgroups_table = sa.sql.table('subgroups',
         sa.Column('id', sa.String(length=5), nullable=False),
         sa.Column('groupname', sa.String),
         sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
         sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    )

    uids = set()

    while len(uids) != 5:
        uid = ''.join(random.sample(string.ascii_lowercase + string.digits, 5))
        uids.add(uid)

    uids = list(uids)

    data = []

    member_uid = uids[-4]

    for group in ['AMBASSADOR', 'INVESTOR', 'HOSTER', 'MEMBER', 'PUBLIC']:
        data.append({
            'id': uids.pop(),
            'groupname': group,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })

    op.bulk_insert(subgroups_table, data)


    contact_subgroups = sa.sql.table('contacts_subgroups',
                                   sa.Column('subgroup_id', sa.String),
                                   sa.Column('contact_id', sa.String)
    )

    conn = op.get_bind()

    res = conn.execute(
        "select id from contacts"
    )

    data = []
    db_results = res.fetchall()
    for result in db_results:
        data.append({
            'contact_id': result['id'],
            'subgroup_id': member_uid
        })

    op.bulk_insert(contact_subgroups, data)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    tbl, data = get_contact_old_addresses()

    op.drop_column('contacts', 'country')

    COUNTRIES.create(op.get_bind(), checkfirst=True)

    op.create_table('subgroups',
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('groupname', sa.Enum('AMBASSADOR', 'INVESTOR', 'HOSTER', 'MEMBER', 'PUBLIC', name='subgroupname'), nullable=True),
    sa.Column('author_last_id', sa.String(length=5), nullable=True),
    sa.Column('author_original_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companytags',
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('tag', sa.String(length=20), nullable=False),
    sa.Column('company_id', sa.String(length=5), nullable=True),
    sa.Column('author_last_id', sa.String(length=5), nullable=True),
    sa.Column('author_original_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts_subgroups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subgroup_id', sa.String(length=5), nullable=True),
    sa.Column('contact_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['subgroup_id'], ['subgroups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addresses',
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('street_number', sa.String(length=255), nullable=True),
    sa.Column('street_name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=True),
    sa.Column('state', sa.Text(), nullable=True),
    sa.Column('zip_code', sa.String(length=255), nullable=True),
    sa.Column('country', COUNTRIES, nullable=True),
    sa.Column('contact_id', sa.String(length=5), nullable=True),
    sa.Column('company_id', sa.String(length=5), nullable=True),
    sa.Column('deal_id', sa.String(length=5), nullable=True),
    sa.Column('author_last_id', sa.String(length=5), nullable=True),
    sa.Column('author_original_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['deal_id'], ['deals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('contacts', sa.Column('referral_code', sa.String(length=255), nullable=True))
    op.add_column('contacts', sa.Column('tf_app', sa.Boolean(), nullable=True))
    op.add_column('contacts', sa.Column('tf_web', sa.Boolean(), nullable=True))
    op.drop_column('contacts', 'street_number')
    op.drop_column('contacts', 'street_name')
    op.drop_column('contacts', 'zip_code')
    op.add_column('deals', sa.Column('referral_code', sa.String(length=255), nullable=True))

    # populate new addresses
    op.bulk_insert(tbl, data)

    add_contact_subgroups()

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deals', 'referral_code')
    op.add_column('contacts', sa.Column('zip_code', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('contacts', sa.Column('country', postgresql.ENUM('Denmark', 'Sudan', 'Guadeloupe', 'Zambia', 'Samoa', 'Georgia', 'Bulgaria', 'French Guiana', 'Cyprus', 'French Polynesia', 'United Arab Emirates', 'Tonga', 'Myanmar', 'Libyan Arab Jamahiriya', 'Mexico', 'Ukraine', 'Ecuador', 'Togo', 'Oman', 'Estonia', 'Haiti', 'Italy', 'Japan', 'Burkina Faso', 'Saint Lucia', 'Germany', 'Turkmenistan', 'United States Minor Outlying Islands', 'Paraguay', 'Greenland', 'Czech Republic', 'Honduras', 'Virgin Islands, British', 'Saint Kitts and Nevis', 'Ghana', 'Serbia and Montenegro', 'Cocos (Keeling) Islands', 'Romania', 'China', 'Iran, Islamic Republic of', 'Aruba', "Korea, Democratic People's Republic of", 'Hungary', 'Finland', 'British Indian Ocean Territory', 'Belize', 'Liechtenstein', 'Slovenia', 'Gambia', 'Canada', 'Christmas Island', 'Barbados', 'Austria', 'Guinea-Bissau', 'Gibraltar', 'San Marino', 'Pitcairn', 'Palestinian Territory, Occupied', 'Dominican Republic', 'Equatorial Guinea', 'Fiji', 'Benin', 'Guinea', 'France', 'Cameroon', 'South Africa', 'New Caledonia', 'Falkland Islands (Malvinas)', 'Djibouti', 'Nauru', 'Lesotho', 'Palau', 'Yemen', 'Martinique', 'Guam', 'Liberia', 'Angola', 'Taiwan, Province of China', 'Congo, the Democratic Republic of the', 'Rwanda', 'Western Sahara', 'Thailand', 'Uzbekistan', 'Israel', 'Algeria', 'Azerbaijan', 'Heard Island and Mcdonald Islands', 'Cape Verde', 'Maldives', 'Zimbabwe', 'Puerto Rico', 'Brunei Darussalam', 'Guatemala', 'Jamaica', 'Mauritius', 'Kuwait', 'Croatia', 'Bhutan', 'Somalia', 'United Kingdom', "Cote D'Ivoire", 'Mauritania', 'Australia', 'Mayotte', 'Macao', 'South Georgia and the South Sandwich Islands', 'Burundi', 'Uruguay', 'Seychelles', 'Kyrgyzstan', 'Saint Vincent and the Grenadines', 'Hong Kong', 'Chile', 'Ethiopia', 'Iceland', 'Kenya', 'Belarus', 'Greece', 'Swaziland', 'Solomon Islands', 'Lithuania', 'Malawi', 'Norway', 'Cuba', 'Latvia', 'Nigeria', 'Portugal', 'Iraq', 'Grenada', 'Bosnia and Herzegovina', 'United States', 'Sweden', 'Sao Tome and Principe', 'Holy See (Vatican City State)', 'Egypt', 'Mali', 'Antigua and Barbuda', 'Mongolia', 'French Southern Territories', 'Lebanon', 'Reunion', 'Eritrea', 'Vanuatu', 'Singapore', 'Turkey', 'Philippines', 'Turks and Caicos Islands', 'Svalbard and Jan Mayen', 'Panama', 'Montserrat', 'Colombia', 'Saint Helena', 'Slovakia', 'Botswana', 'El Salvador', 'Bahrain', 'Tajikistan', 'Saint Pierre and Miquelon', 'Niue', 'Bermuda', 'Morocco', 'Madagascar', 'Central African Republic', 'Chad', 'Ireland', 'Comoros', 'Northern Mariana Islands', 'Tanzania, United Republic of', 'Wallis and Futuna', 'Malta', 'Sri Lanka', 'Cambodia', 'Viet Nam', 'Macedonia, the Former Yugoslav Republic of', 'Indonesia', 'Papua New Guinea', 'Uganda', 'Venezuela', 'Korea, Republic of', 'Mozambique', 'Argentina', 'Congo', 'Belgium', 'Antarctica', 'Tuvalu', 'Gabon', 'India', 'Kiribati', 'Pakistan', 'Spain', 'Bouvet Island', 'Bahamas', 'Peru', 'Afghanistan', 'Malaysia', 'Niger', 'Qatar', 'Netherlands Antilles', 'Armenia', 'Tunisia', 'Russian Federation', 'Guyana', 'Switzerland', 'American Samoa', 'Suriname', 'Luxembourg', 'Sierra Leone', 'Cayman Islands', 'Cook Islands', 'New Zealand', 'Micronesia, Federated States of', 'Marshall Islands', 'Trinidad and Tobago', 'Monaco', 'Moldova, Republic of', 'Syrian Arab Republic', 'Bolivia', 'Norfolk Island', 'Poland', 'Senegal', 'Costa Rica', 'Brazil', 'Anguilla', 'Virgin Islands, U.s.', "Lao People's Democratic Republic", 'Nicaragua', 'Dominica', 'Netherlands', 'Namibia', 'Jordan', 'Andorra', 'Bangladesh', 'Kazakhstan', 'Albania', 'Nepal', 'Saudi Arabia', 'Faroe Islands', 'Timor-Leste', 'Tokelau', name='countries'), autoincrement=False, nullable=True))
    op.add_column('contacts', sa.Column('street_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('contacts', sa.Column('street_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('contacts', 'tf_web')
    op.drop_column('contacts', 'tf_app')
    op.drop_column('contacts', 'referral_code')
    op.drop_table('addresses')
    op.drop_table('contacts_subgroups')
    op.drop_table('companytags')
    op.drop_table('subgroups')
    # ### end Alembic commands ###
