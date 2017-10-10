# Accessing Graphql API using HTTP client

Our end point where Graphql API is exposed is ```/api```

## Python


- Example on a mutation (Adding a contact)
    - Example on errors
        ```python

        create_contact_mutation = """
            mutation{
                createContact( first_name: "hamdy", emails: "d@d.com", telephones: "123"){
                    contact {
                        uid
                    }
                }
            }"""


        payload = {'query':create_contact_mutation}
        headers = {'Content-Type':'application/json'}
        data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)

        data.ok # False

        data.json()

        # Result looks like
        {'errors': ['Unknown argument "first_name" on field "createContact" of type "Mutations". Did you mean "firstname" or "lastname"?',
          'Field "createContact" argument "firstname" of type "String!" is required but not provided.']}
        ```
    - Example on success
        ```python

        create_contact_mutation = """
            mutation{
                createContact( firstname: "hamdy", emails: "d@d.com", telephones: "123"){
                    contact {
                        uid
                    }
                }
            }"""


        payload = {'query':create_contact_mutation}
        headers = {'Content-Type':'application/json'}
        data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)

        data.ok # True
        data.json()

        {'contact': {'uid': 'lc90r'}}

        ```

- Examples on a queries

     ```python

        query = """
            {
                contacts(first: 3){
                    edges{
                        nodes{
                            firstname
                            lastname
                            uid
                        }
                    }
                 }
            }"""


        payload = {'query':query}
        headers = {'Content-Type':'application/json'}
        data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)

        data.ok # True
        data.json()

        [{'firstname': 'fathy', 'lastname': '', 'uid': 'qkted'},
         {'firstname': 'fathy3', 'lastname': '', 'uid': '0urxf'},
         {'firstname': 'fathy4', 'lastname': '', 'uid': '3yfbt'}]
     ```


     ```python

        query = """
            {
                contact(uid: "qkted"){
                    firstname
                    lastname
                    uid
                 }
            }"""


        payload = {'query':query}
        headers = {'Content-Type':'application/json'}
        data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)

        data.ok # True
        data.json()

        {'firstname': 'fathy', 'lastname': '', 'uid': 'qkted'}
     ```


     ```python

        query = """
            {
                contact(uid: "non-existent-uid"){
                    firstname
                    lastname
                    uid
                 }
            }"""


        payload = {'query':query}
        headers = {'Content-Type':'application/json'}
        data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)

        data.ok # False
        data.status_code # 404
        ```


## Developing applications for the CRM
You need to create organization and added it to crm_users organization

```
import requests
host = "https://itsyou.online"
client_id = APPID
client_secret = APPSECRET


print('Getting access token')
r = requests.post('{}/v1/oauth/access_token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
    host, client_id, client_secret), verify=False)
if r.status_code != 200:
    raise Exception('Response code {} - {}'.format(r.status_code, r.text))
print(r.text)
access_token = r.json()['access_token']
username = r.json()['info']['username']

print('Getting the user object using the token in the query parameters')
r = requests.get('{}/api/users/{}?access_token={}'.format(host,
                                                          username, access_token), verify=False)
print('{} - {}'.format(r.status_code, r.text))

print('Getting the user object using the token in the Authorization header')
r = requests.get('{}/api/users/{}'.format(host, username),
                 headers={'Authorization': 'token {}'.format(access_token)}, verify=False)
print('{} - {}'.format(r.status_code, r.text))

base_url = "https://itsyou.online/v1/oauth/jwt"
headers = {'Authorization': 'token %s' % access_token}
data = {'scope': 'user:memberOf:%s' % "simple_crm.crm_users"}
response = requests.post(
    base_url, json=data, headers=headers, verify=False)
jwt = response.content.decode()
print(jwt, "\n")
from jose.jwt import get_unverified_claims

print(get_unverified_claims(jwt))

query = "query allusers { users { id, username} }"
headers = {"Authorization": "bearer {jwt}".format(jwt=jwt)}

res = requests.post("http://localhost:10000/api",
                    headers=headers, json={'query': query})
print(res.json())
```