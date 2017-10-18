## Configuration

- Main config file is ```settings.py``` all other config files import it; So ```settings.py``` holds sared configrations among all environments
- All production related settings goes for ```settings.prod.py```
- All development related settings goes for ```settings.dev.py```

### Dev Environment
CRM is built around the usage of IYO for authentication. Typical setup will include a Caddy [configured with IYO plugin](https://github.com/itsyouonline/caddy-integration) as a reverse proxy to CRM application  

> Recommended way to install caddy and its plugins is using [Caddyman](https://github.com/Incubaid/caddyman)
#### Example

- For local setup if you're running caddy from same crm DIR
    ```

    :10000 {         #this is the port you want to forward the website to
        proxy / localhost:5000 {
            header_upstream Host "localhost:10000"
            except /docs/graphqlapi
        }
        browse /docs/graphqlapi/ ./docs/graphqlapi/index.html
        oauth {
            client_id       crm
            client_secret   j_V4qVf6dLwWR_jeQNVrKvkJQ-KymN7D011zFu15H8a4lg9ldx23
            redirect_url    http://localhost:10000/iyo_callback
            authentication_required /             #that means no authentication required
            extra_scopes	user:address,user:email,user:phone,user:memberof:crm.crm_users
            allow_extension api
            allow_extension graphqlapi
            allow_extension html
            allow_extension png

        }
    }
    ```

- For production
    You may want to change ```browse /docs/graphqlapi/ ./docs/graphqlapi/index.html``` into:
    ```
        root /opt/code/github/incubaid/crm/
        browse docs/graphqlapi/index.html
    ```

**oauth**

- Here we configure caddy to accept authentication to people member of organization `crm.crm_users` and skipping the iyo authentication flow for routes on `api`, `graphql`, `png` and we use the `/docs/graphqlapi` endpoint using the `browse` directive.
