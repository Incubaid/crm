"""empty message

Revision ID: 0bfd4e50a2a7
Revises: fd18a2dca3a5
Create Date: 2017-11-14 15:02:14.782605

"""
import random
import string

from alembic import op
import sqlalchemy as sa
from future.backports import datetime
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0bfd4e50a2a7'
down_revision = 'fd18a2dca3a5'
branch_labels = None
depends_on = None


def get_addresses_countries():
    countries = {v:k for k, v in {
        "AF": "Afghanistan",
        "AL": "Albania",
        "DZ": "Algeria",
        "AS": "American Samoa",
        "AD": "Andorra",
        "AO": "Angola",
        "AI": "Anguilla",
        "AQ": "Antarctica",
        "AG": "Antigua and Barbuda",
        "AR": "Argentina",
        "AM": "Armenia",
        "AW": "Aruba",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BS": "Bahamas",
        "BH": "Bahrain",
        "BD": "Bangladesh",
        "BB": "Barbados",
        "BY": "Belarus",
        "BE": "Belgium",
        "BZ": "Belize",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BT": "Bhutan",
        "BO": "Bolivia",
        "BA": "Bosnia and Herzegovina",
        "BW": "Botswana",
        "BV": "Bouvet Island",
        "BR": "Brazil",
        "IO": "British Indian Ocean Territory",
        "BN": "Brunei Darussalam",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CA": "Canada",
        "CV": "Cape Verde",
        "KY": "Cayman Islands",
        "CF": "Central African Republic",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CX": "Christmas Island",
        "CC": "Cocos (Keeling) Islands",
        "CO": "Colombia",
        "KM": "Comoros",
        "CG": "Congo",
        "CD": "Congo, the Democratic Republic of the",
        "CK": "Cook Islands",
        "CR": "Costa Rica",
        "CI": "Cote D'Ivoire",
        "HR": "Croatia",
        "CU": "Cuba",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "DK": "Denmark",
        "DJ": "Djibouti",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EG": "Egypt",
        "SV": "El Salvador",
        "GQ": "Equatorial Guinea",
        "ER": "Eritrea",
        "EE": "Estonia",
        "ET": "Ethiopia",
        "FK": "Falkland Islands (Malvinas)",
        "FO": "Faroe Islands",
        "FJ": "Fiji",
        "FI": "Finland",
        "FR": "France",
        "GF": "French Guiana",
        "PF": "French Polynesia",
        "TF": "French Southern Territories",
        "GA": "Gabon",
        "GM": "Gambia",
        "GE": "Georgia",
        "DE": "Germany",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GR": "Greece",
        "GL": "Greenland",
        "GD": "Grenada",
        "GP": "Guadeloupe",
        "GU": "Guam",
        "GT": "Guatemala",
        "GN": "Guinea",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HT": "Haiti",
        "HM": "Heard Island and Mcdonald Islands",
        "VA": "Holy See (Vatican City State)",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungary",
        "IS": "Iceland",
        "IN": "India",
        "ID": "Indonesia",
        "IR": "Iran, Islamic Republic of",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IL": "Israel",
        "IT": "Italy",
        "JM": "Jamaica",
        "JP": "Japan",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KI": "Kiribati",
        "KP": "Korea, Democratic People's Republic of",
        "KR": "Korea, Republic of",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "LA": "Lao People's Democratic Republic",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LS": "Lesotho",
        "LR": "Liberia",
        "LY": "Libyan Arab Jamahiriya",
        "LI": "Liechtenstein",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MO": "Macao",
        "MK": "Macedonia, the Former Yugoslav Republic of",
        "MG": "Madagascar",
        "MW": "Malawi",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MH": "Marshall Islands",
        "MQ": "Martinique",
        "MR": "Mauritania",
        "MU": "Mauritius",
        "YT": "Mayotte",
        "MX": "Mexico",
        "FM": "Micronesia, Federated States of",
        "MD": "Moldova, Republic of",
        "MC": "Monaco",
        "MN": "Mongolia",
        "MS": "Montserrat",
        "MA": "Morocco",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NL": "Netherlands",
        "AN": "Netherlands Antilles",
        "NC": "New Caledonia",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NE": "Niger",
        "NG": "Nigeria",
        "NU": "Niue",
        "NF": "Norfolk Island",
        "MP": "Northern Mariana Islands",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PW": "Palau",
        "PS": "Palestinian Territory, Occupied",
        "PA": "Panama",
        "PG": "Papua New Guinea",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PN": "Pitcairn",
        "PL": "Poland",
        "PT": "Portugal",
        "PR": "Puerto Rico",
        "QA": "Qatar",
        "RE": "Reunion",
        "RO": "Romania",
        "RU": "Russian Federation",
        "RW": "Rwanda",
        "SH": "Saint Helena",
        "KN": "Saint Kitts and Nevis",
        "LC": "Saint Lucia",
        "PM": "Saint Pierre and Miquelon",
        "VC": "Saint Vincent and the Grenadines",
        "WS": "Samoa",
        "SM": "San Marino",
        "ST": "Sao Tome and Principe",
        "SA": "Saudi Arabia",
        "SN": "Senegal",
        "CS": "Serbia and Montenegro",
        "SC": "Seychelles",
        "SL": "Sierra Leone",
        "SG": "Singapore",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "SB": "Solomon Islands",
        "SO": "Somalia",
        "ZA": "South Africa",
        "GS": "South Georgia and the South Sandwich Islands",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SR": "Suriname",
        "SJ": "Svalbard and Jan Mayen",
        "SZ": "Swaziland",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syrian Arab Republic",
        "TW": "Taiwan, Province of China",
        "TJ": "Tajikistan",
        "TZ": "Tanzania, United Republic of",
        "TH": "Thailand",
        "TL": "Timor-Leste",
        "TG": "Togo",
        "TK": "Tokelau",
        "TO": "Tonga",
        "TT": "Trinidad and Tobago",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TM": "Turkmenistan",
        "TC": "Turks and Caicos Islands",
        "TV": "Tuvalu",
        "UG": "Uganda",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "GB": "United Kingdom",
        "US": "United States",
        "UM": "United States Minor Outlying Islands",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VU": "Vanuatu",
        "VE": "Venezuela",
        "VN": "Viet Nam",
        "VG": "Virgin Islands, British",
        "VI": "Virgin Islands, U.s.",
        "WF": "Wallis and Futuna",
        "EH": "Western Sahara",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe"
    }.items()}
    address_country = {}
    for record in op.get_bind().execute('select id,country from addresses').fetchall():
        address_country[record[0]] = countries[record[1]]
    return address_country


def get_uids(length):
    uids = set()
    while len(uids) != length:
        uid = ''.join(random.sample(string.ascii_lowercase + string.digits, 5))
        uids.add(uid)
    return list(uids)

def update_currencies():
    currencies = op.create_table('currencies',
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('id', sa.String(length=5), nullable=False),
                    sa.Column('name', sa.String(length=3), nullable=False),
                    sa.Column('value_usd', sa.Float(), nullable=True),
                    sa.Column('author_original_id', sa.String(length=5), nullable=True),
                    sa.Column('author_last_id', sa.String(length=5), nullable=True),
                    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


    inserted_currencies = {
        'USD': 'xawe0'
    }

    uids = ['xawe1', 'xawe2', 'xawe3', 'xawe4']

    for record in op.get_bind().execute('select currency,value_usd from currency_exchange').fetchall():
        id = uids.pop(0)

        inserted_currencies[record[0]] = id

        op.bulk_insert(
            currencies,
            [
                {'id': id, 'created_at': datetime.datetime.now(), 'updated_at': datetime.datetime.now(), 'name': record[0], 'value_usd': record[1]},
            ]
        )
    op.add_column('deals', sa.Column('currency_id', sa.String(length=5), nullable=True))
    op.create_foreign_key(None, 'deals', 'currencies', ['currency_id'], ['id'])

    # new migration don't add any data
    if len(inserted_currencies) > 1:
        op.bulk_insert(
            currencies,
            [
                {'id': 'xawe0', 'created_at': datetime.datetime.now(), 'updated_at': datetime.datetime.now(),
                 'name': 'USD',
                 'value_usd': 1.0},
            ]
        )
        for item in op.get_bind().execute('select id, currency from deals').fetchall():
            id = item[0]
            currency_id = inserted_currencies[item[1]]
            op.get_bind().execute("update deals set currency_id='%s' where id='%s'" % (currency_id, id))

        op.get_bind().execute("update deals set currency_id='xawe0' where currency_id is null")

    op.alter_column('deals', 'currency_id',
                    existing_type=sa.VARCHAR(length=5),
                    nullable=False)

    op.alter_column('deals', 'deal_state',
                    existing_type=postgresql.ENUM('NEW', 'INTERESTED', 'CONFIRMED', 'PENDING', 'CLOSED',
                                                  name='dealstate'),
                    nullable=False)
    op.alter_column('deals', 'deal_type',
                    existing_type=postgresql.ENUM('HOSTER', 'ITO', 'PTO', 'AMBASSADOR', 'ITFT', name='dealtype'),
                    nullable=False)

    op.get_bind().execute('update deals set value=0.0 where value is null')

    op.alter_column('deals', 'value',
                    existing_type=postgresql.DOUBLE_PRECISION(precision=53),
                    nullable=False)

    op.drop_index('ix_deals_currency', table_name='deals')
    op.drop_column('deals', 'currency')
    op.drop_table('currency_exchange')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    update_currencies()

    addresses_countries = get_addresses_countries()
    op.get_bind().execute('drop type countries cascade')

    op.create_table('countries',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('name', sa.Enum('BZ', 'GD', 'TM', 'CO', 'BM', 'SG', 'TC', 'DZ', 'WF', 'MS', 'BO', 'ST', 'MO', 'TN', 'AS', 'AI', 'SZ', 'CD', 'NR', 'SK', 'LV', 'VE', 'MZ', 'NP', 'RU', 'WS', 'CF', 'CA', 'AN', 'VI', 'NE', 'EC', 'GN', 'KZ', 'CH', 'KW', 'IN', 'NA', 'SO', 'GH', 'BJ', 'NI', 'PF', 'KY', 'MP', 'SM', 'PG', 'HU', 'CC', 'AD', 'NU', 'FJ', 'DO', 'PT', 'SC', 'ZW', 'IL', 'LS', 'TV', 'RE', 'MQ', 'BW', 'ZM', 'LA', 'PM', 'UM', 'SN', 'CS', 'JP', 'VU', 'UG', 'IT', 'BB', 'GR', 'AW', 'JO', 'KP', 'MN', 'NO', 'DK', 'LR', 'BD', 'MH', 'DM', 'MX', 'SV', 'VN', 'NC', 'BS', 'MM', 'YE', 'TF', 'KN', 'KE', 'NG', 'KH', 'NL', 'BH', 'NF', 'IS', 'ES', 'GF', 'GM', 'SE', 'DJ', 'JM', 'IE', 'EH', 'NZ', 'MK', 'VC', 'CN', 'TR', 'IQ', 'LI', 'ML', 'TO', 'TH', 'MA', 'PK', 'RO', 'EG', 'FK', 'CM', 'BT', 'SA', 'DE', 'FI', 'BF', 'SH', 'GA', 'AT', 'MT', 'TJ', 'PL', 'LU', 'TG', 'GS', 'PN', 'US', 'BY', 'HK', 'AF', 'CY', 'EE', 'MV', 'AU', 'LT', 'PA', 'BG', 'KI', 'CV', 'MD', 'CI', 'CL', 'SL', 'ID', 'AL', 'AM', 'CX', 'GQ', 'PY', 'MW', 'GT', 'CR', 'ZA', 'BR', 'CU', 'SJ', 'ET', 'VG', 'MG', 'TT', 'UA', 'TL', 'VA', 'MY', 'IR', 'HN', 'HR', 'SY', 'BI', 'ER', 'PR', 'AE', 'AR', 'PW', 'TZ', 'HT', 'MR', 'CZ', 'PE', 'KM', 'LB', 'CK', 'TD', 'RW', 'MC', 'OM', 'LY', 'FM', 'BV', 'GU', 'KG', 'SI', 'GP', 'PH', 'GI', 'GB', 'FR', 'UZ', 'IO', 'HM', 'BN', 'AQ', 'TW', 'AG', 'GY', 'LC', 'SR', 'SD', 'CG', 'GW', 'MU', 'BE', 'PS', 'LK', 'SB', 'AZ', 'AO', 'UY', 'YT', 'TK', 'GE', 'KR', 'FO', 'GL', 'QA', 'BA', name='countriesenum'), nullable=True),
    sa.Column('author_original_id', sa.String(length=5), nullable=True),
    sa.Column('author_last_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_countries_name'), 'countries', ['name'], unique=True)

    op.create_index(op.f('ix_currencies_name'), 'currencies', ['name'], unique=True)
    op.create_table('contacts_countries',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.String(length=5), nullable=True),
    sa.Column('contact_id', sa.String(length=5), nullable=True),
    sa.Column('author_original_id', sa.String(length=5), nullable=True),
    sa.Column('author_last_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('passports',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('passport_fullname', sa.String(length=255), nullable=False),
    sa.Column('passport_number', sa.Text(), nullable=False),
    sa.Column('issuance_date', sa.Date(), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=False),
    sa.Column('country_id', sa.String(length=5), nullable=True),
    sa.Column('contact_id', sa.String(length=5), nullable=True),
    sa.Column('author_original_id', sa.String(length=5), nullable=True),
    sa.Column('author_last_id', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passports_passport_fullname'), 'passports', ['passport_fullname'], unique=False)
    op.create_index(op.f('ix_passports_passport_number'), 'passports', ['passport_number'], unique=False)

    op.add_column('addresses', sa.Column('country_id', sa.String(length=5), nullable=True))

    op.create_foreign_key(None, 'addresses', 'countries', ['country_id'], ['id'])

    op.add_column('contacts', sa.Column('date_of_birth', sa.Date(), nullable=True))

    genders = sa.Enum(u'MALE', u'FEMALE', name='gender')
    genders.create(op.get_bind(), checkfirst=True)

    op.add_column('contacts', sa.Column('gender', genders, nullable=True))
    op.create_index(op.f('ix_contacts_gender'), 'contacts', ['gender'], unique=False)

    op.add_column('links', sa.Column('message_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'links', 'messages', ['message_id'], ['id'])

    msg_states = sa.Enum(u'TOSEND', u'SENT', u'FAILED', name='messagestate')
    msg_states.create(op.get_bind(), checkfirst=True)
    op.add_column('messages', sa.Column('state', msg_states, nullable=True))
    op.create_index(op.f('ix_messages_state'), 'messages', ['state'], unique=False)
    op.alter_column('tags', 'tag',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_tags_tag', table_name='tags')
    op.create_index(op.f('ix_tags_tag'), 'tags', ['tag'], unique=True)


    # Update Addresses table with new countries

    countries = sa.sql.table('countries',
                 sa.Column('id', sa.String(length=5), nullable=False),
                 sa.Column('name', sa.String),
                 sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                 sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
                 )

    uids = get_uids(len(addresses_countries))

    for id, country in addresses_countries.items():
        q = op.get_bind().execute("select id from countries where name='%s';" % country).fetchall()
        if len(q) > 0:
            uid = q[0][0]
        else:
            uid = uids.pop()
            op.bulk_insert(
                countries,
                [
                    {'id': uid, 'created_at': datetime.datetime.now(), 'updated_at': datetime.datetime.now(),
                     'name': country,
                     'value_usd': 1.0
                     },
                ]
            )

        op.get_bind().execute("update addresses set country_id='%s' where id='%s'" % (uid, id))

        # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tags_tag'), table_name='tags')
    op.create_index('ix_tags_tag', 'tags', ['tag'], unique=False)
    op.alter_column('tags', 'tag',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_messages_state'), table_name='messages')
    op.drop_column('messages', 'state')
    op.drop_constraint(None, 'links', type_='foreignkey')
    op.drop_column('links', 'message_id')
    op.add_column('deals', sa.Column('currency', postgresql.ENUM('USD', 'EUR', 'AED', 'GBP', 'BTC', name='dealcurrency'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'deals', type_='foreignkey')
    op.create_index('ix_deals_currency', 'deals', ['currency'], unique=False)
    op.drop_column('deals', 'currency_id')
    op.drop_index(op.f('ix_contacts_gender'), table_name='contacts')
    op.drop_column('contacts', 'gender')
    op.drop_column('contacts', 'date_of_birth')
    op.add_column('addresses', sa.Column('country', postgresql.ENUM('Czech Republic', 'Nepal', 'Switzerland', 'Papua New Guinea', 'Australia', 'Kyrgyzstan', 'Antigua and Barbuda', 'Qatar', 'Pakistan', 'Ecuador', 'Palau', 'Mongolia', 'Comoros', 'Nauru', 'Belgium', 'Portugal', 'Sweden', 'Liberia', 'Kuwait', 'Brazil', 'Canada', 'Angola', 'Trinidad and Tobago', 'Cape Verde', 'Mauritius', 'Samoa', 'Ethiopia', 'Saint Vincent and the Grenadines', 'Anguilla', 'Senegal', 'Reunion', 'Morocco', 'Costa Rica', 'French Southern Territories', "Korea, Democratic People's Republic of", 'Tuvalu', 'Saint Kitts and Nevis', 'Guyana', 'Bangladesh', 'Tokelau', 'Afghanistan', 'Egypt', 'Peru', 'Moldova, Republic of', 'Rwanda', 'British Indian Ocean Territory', 'Albania', 'Philippines', 'Serbia and Montenegro', 'Lithuania', 'Mayotte', 'Saint Helena', 'Mexico', 'Timor-Leste', 'Central African Republic', 'Equatorial Guinea', 'Saudi Arabia', 'Bahamas', 'Tunisia', 'Kenya', 'United States', 'South Georgia and the South Sandwich Islands', 'Panama', 'Poland', 'Puerto Rico', 'Macedonia, the Former Yugoslav Republic of', 'Jamaica', 'Bolivia', 'Croatia', 'Virgin Islands, British', 'Chad', 'Marshall Islands', 'Italy', 'Monaco', 'Norfolk Island', 'Taiwan, Province of China', 'Grenada', 'Haiti', 'Slovenia', 'Zimbabwe', 'Namibia', 'Holy See (Vatican City State)', 'Malawi', 'Macao', 'Zambia', 'Faroe Islands', 'Vanuatu', 'Iceland', 'Iraq', 'Uruguay', 'New Caledonia', 'New Zealand', 'Kazakhstan', 'Togo', 'United Arab Emirates', 'French Polynesia', 'Netherlands Antilles', 'Armenia', 'Maldives', 'Denmark', 'Honduras', 'Lebanon', 'Cambodia', 'Chile', 'Cyprus', 'Tajikistan', 'Latvia', 'Jordan', 'Niue', 'Fiji', 'Northern Mariana Islands', 'Ireland', 'Guadeloupe', 'Cocos (Keeling) Islands', 'Yemen', 'Svalbard and Jan Mayen', 'French Guiana', 'Turkey', 'Sierra Leone', 'Germany', 'Syrian Arab Republic', 'Libyan Arab Jamahiriya', 'Gabon', 'Antarctica', 'Dominica', 'Ukraine', 'Korea, Republic of', 'Niger', 'Martinique', 'Nigeria', 'Virgin Islands, U.s.', 'Dominican Republic', 'Pitcairn', 'Malta', 'Turks and Caicos Islands', 'Viet Nam', 'Burundi', 'Swaziland', 'Argentina', "Lao People's Democratic Republic", 'Malaysia', 'Solomon Islands', 'Venezuela', 'Andorra', 'Christmas Island', 'Botswana', 'Mauritania', 'Myanmar', 'United States Minor Outlying Islands', 'Bulgaria', 'Bahrain', 'Lesotho', "Cote D'Ivoire", 'Congo', 'Belize', 'Bosnia and Herzegovina', 'Sudan', 'Spain', 'Iran, Islamic Republic of', 'Barbados', 'Somalia', 'Netherlands', 'Gibraltar', 'United Kingdom', 'Bermuda', 'Kiribati', 'Brunei Darussalam', 'Saint Lucia', 'Heard Island and Mcdonald Islands', 'South Africa', 'Palestinian Territory, Occupied', 'Austria', 'Greece', 'Mali', 'Singapore', 'France', 'Falkland Islands (Malvinas)', 'Romania', 'Finland', 'Cuba', 'Georgia', 'Guinea-Bissau', 'Bouvet Island', 'Uzbekistan', 'Hong Kong', 'Wallis and Futuna', 'Gambia', 'American Samoa', 'Aruba', 'Cook Islands', 'Israel', 'Cayman Islands', 'Estonia', 'Uganda', 'Madagascar', 'Greenland', 'Djibouti', 'Belarus', 'Liechtenstein', 'Tonga', 'San Marino', 'Sao Tome and Principe', 'Azerbaijan', 'Suriname', 'Ghana', 'Benin', 'Western Sahara', 'Bhutan', 'Guam', 'Seychelles', 'Nicaragua', 'Japan', 'Guinea', 'Cameroon', 'Saint Pierre and Miquelon', 'Slovakia', 'Micronesia, Federated States of', 'Montserrat', 'Algeria', 'Oman', 'Eritrea', 'Burkina Faso', 'Indonesia', 'Colombia', 'Norway', 'Congo, the Democratic Republic of the', 'China', 'Thailand', 'Russian Federation', 'Hungary', 'Guatemala', 'India', 'Turkmenistan', 'Paraguay', 'El Salvador', 'Tanzania, United Republic of', 'Sri Lanka', 'Mozambique', 'Luxembourg', name='countries'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'addresses', type_='foreignkey')
    op.create_index('ix_addresses_country', 'addresses', ['country'], unique=False)
    op.drop_column('addresses', 'country_id')
    op.create_table('currency_exchange',
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('id', sa.VARCHAR(length=5), autoincrement=False, nullable=False),
    sa.Column('currency', postgresql.ENUM('USD', 'EUR', 'AED', 'GBP', 'BTC', name='dealcurrency'), autoincrement=False, nullable=True),
    sa.Column('value_usd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('author_last_id', sa.VARCHAR(length=5), autoincrement=False, nullable=True),
    sa.Column('author_original_id', sa.VARCHAR(length=5), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_last_id'], ['users.id'], name='currency_exchange_author_last_id_fkey'),
    sa.ForeignKeyConstraint(['author_original_id'], ['users.id'], name='currency_exchange_author_original_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='currency_exchange_pkey')
    )
    op.drop_index(op.f('ix_passports_passport_number'), table_name='passports')
    op.drop_index(op.f('ix_passports_passport_fullname'), table_name='passports')
    op.drop_table('passports')
    op.drop_table('contacts_countries')
    op.drop_index(op.f('ix_currencies_name'), table_name='currencies')
    op.drop_table('currencies')
    op.drop_index(op.f('ix_countries_name'), table_name='countries')
    op.drop_table('countries')
    # ### end Alembic commands ###
