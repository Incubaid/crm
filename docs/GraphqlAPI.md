## Graphql API

### Contacts

**Mutations**

- ```createcontacts(firsrecords=[{firstname: "Sandra", lastname:"", description:"", telegram:"", bio: "", emails:"", telephones:"", belief_statement:"", owner_id:"", ownerbackup_id:"", parent_id:"", tf_app:true, tf_web:false, message_channels:"", country:"Brazil"}])```
    - required
        records

    - Each record is a dict of contact fileds with the following required fields
        - firstname
        - country [Check available choices](https://github.com/Incubaid/crm/blob/master/crm/countries.py) Afghanistan, Albania, ..
        - emails
        - telephones

- ```deletecontacts(uids=["id1", "id2"])```
   - required
    - uids

- ```updatecontacts(records=[{'uid':'x0O2', 'firstname': 'hamdy'}])```
    - required
        records
    - Each record is a a dict of contact fileds with the following required fields
        - uid

**Queries**
- ```contacts```
- ```contact(uid="uid")```


### Deals

**Mutations**

- ```createdeals(records=[{name: "deal1", dealState:"NEW", dealType: "HOSTER", currency: "EUR", description:"", closed_at:"2010-01-01",  company_id:"xszss",contact_id:"hhjjs", referral_code:"code"}])```
    - required
        records
    - Each record is a dict of a deal with the following required fields:
        - name
        - dealType :: (HOSTER, ITO, PTO, AMBASSADOR)
        - dealState :: (NEW, INTERESTED, CONFIRMED, PENDING, CLOSED)
        - currency :: (USD, EUR, AED, GBP, BTC)

- ```deletedeals(uids=["id1", "id2"])```
   - required
        - uids

- ```updatedeals(records=[{'uid':'x0O2', 'description': 'description'}])```
    - required
        records
    - Each record is a a dict of contact fileds with the following required fields
        - uid

**Queries**
- ```deals```
- ```deal(uid="uid")```
