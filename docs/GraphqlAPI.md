## Graphql API

### Contacts

**Mutations**

- createcontact(firstname: "Sandra", lastname:"", description:"", telegram:"", bio: "", emails:"", telephones:"", belief_statement:"", owner_id:"", ownerbackup_id:"", parent_id:"", tf_app:true, tf_web:false, message_channels:"", country:"Brazil")
    - required
        - firstname
        - country [Check available choices](https://github.com/Incubaid/crm/blob/master/crm/countries.py) Afghanistan, Albania, ..
        - emails
        - telephones

**Queries**
    - contacts
    - contact(uid="uid")


### Deals

**Mutations**

- createdeal(name: "deal1", dealState:"NEW", dealType: "HOSTER", currency: "EUR", description:"", closed_at:"2010-01-01",  company_id:"xszss",contact_id:"hhjjs", referral_code:"code")
    - required:
        - name
        - dealType :: (HOSTER, ITO, PTO, AMBASSADOR)
        - dealState :: (NEW, INTERESTED, CONFIRMED, PENDING, CLOSED)
        - currency :: (USD, EUR, AED, GBP, BTC)

**Queries**
    - deals
    - deal(uid="uid")

