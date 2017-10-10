## Accessing Graphql API using HTTP client

#### Python

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
