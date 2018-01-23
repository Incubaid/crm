# Accessing Graphql API using HTTP client

- Our end point where Graphql API is exposed is ```/api```
- We have the following constraints on users who can access CRM graphql API on production
    - API users Must be users of this organization ```threefold.crm_users``` or its sub organizations on [IYO](https://itsyou.online)

- ```/api``` expects the following headers:
    - ```Content-Type:Application/json```
    - ```Authorization: bearer {your-jwt-token}``` replace ```your-jwt-token``` with your actual token

- If you want to use the API directly **without bothering about authentication** nor [IYO](https://itsyou.online) during Development mode or testing
    - *Disable the ```iyo``` middleware* by setting this environment variable before running application `export EXCLUDED_MIDDLEWARES=iyo`
    - *Don't send Authentication headers in your requests*

- **How to get a JWT token from [IYO](https://itsyou.online) manually**

    - Assuming you created a sub organization from [IYO](https://itsyou.online) ```threefold.crm_users``` organization
    - Get A ```client ID```  & ```Client Secret``` for your organization
        - Go to your organization settings and choose ```API access keys``` then click on (ADD)

            ![Organization settings](assets/iyo-settings1.png)

        - Then make sure your added key allows non UI clients

            ![Organization settings](assets/iyo-settings2.png)
        - Now here's the code snippet to get JWT-Token

            ```python
            import requests
            import urllib

            host = "https://itsyou.online"
            params = {
                'grant_type': 'client_credentials',
                'client_id': 'YOUR-CLIENT-ID', # replace with actual value
                'client_secret': 'YOUR-CLIENT-SECRET' # replace with actual value
            }

            url = '%s/v1/oauth/access_token?%s' % (host, urllib.parse.urlencode(params))

            response = requests.post(url,  verify=False)

            assert(response.status_code == 200)

            result = response.json()

            access_token = result['access_token']

            # Now Getting JWT
            url = '%s/v1/oauth/jwt' % host

            headers = {'Authorization': 'token %s' % access_token}

            data = {'scope': 'user:memberOf:%s' % "simple_crm.crm_users"}

            response = requests.post(
                url,
                json=data,
                headers=headers,
                verify=False)

            assert(response.status_code == 200)

            jwt = response.content.decode()
            ```
- **How to get a JWT token from [IYO](https://itsyou.online) using [Jumpscale framework](https://github.com/Jumpscale/bash)**
    ```python3
    j.clients.openvcloud.getJWTTokenFromItsYouOnline(applicationId, secret, validity=3600)
    ```


# Using the HTTP client


### Python

- **Examples**
    - Example on errors
        ```python
            q = """
                {
                  countries(name:Belgium){
                    edges{
                      node{
                        invalidField
                      }
                    }
                  }
                }
            """

            import requests
            payload = {'query':q}
            headers = {'Content-Type':'application/json', 'Authorization': 'bearer your-jwt-token'} # replace 'your-jwt-token' with actual token
            data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)
            data.ok #False
            data.json()
            {'errors': ['Cannot query field "invalidField" on type "Country".']}
        ```
    - Examples on success
        ```
            q = """
                {
                    country(uid: "g9w57"){
                        authorOriginal{
                            username
                        }
                        name
                    }
                }
            """

            import requests
            payload = {'query':q}
            headers = {'Content-Type':'application/json', 'Authorization': 'bearer your-jwt-token'} # replace 'your-jwt-token' with actual token
            data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)
            data.json()
            {'country': {'authorOriginal': None, 'name': 'Saudi Arabia'}}
        ```

        ```
            q = """
                {
                  countries(name:Belgium){
                    edges{
                      node{
                        name
                      }
                    }
                  }
                }
            """

            import requests
            payload = {'query':q}
            headers = {'Content-Type':'application/json', 'Authorization': 'bearer your-jwt-token'} # replace 'your-jwt-token' with actual token
            data = requests.post('http://127.0.0.1:5000/api', json=payload, headers=headers)
            data.json()
            {'countries': {'edges': [{'node': {'name': 'Belgium'}}]}}
        ```


Everything Goes the same as if you're using `/graphql` endpoint
Please refer to [CRM API General overview](GraphqlQueriesAndMutations.md)
