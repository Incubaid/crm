# incubaidCRM

## Installation
- clone `https://github.com/Incubaid/crm` 
- checkout to `flaskproject` branch.
- `pip install -r requirements.txt`

## Start Application
- If you want to bootstrap it with some test fixtures 
    `bash runappwithfixtures.sh` which is equivalent to `BOOTSTRAPWITHFIXTURES=TRUE python3 app.py`
- If you have database already just execute `python3 app.py`

## Admin Panel
After starting the application you can access the admin panel from http://localhost:5000

## GraphQL
graphQL editor is accessible from http://localhost:5000/graphql
![alt GraphQLInterface](images/graphql.png "GraphQL")
In the editor you can type graphql queries like
```graphql
query allContacts{
  contacts {
    firstname,
    email
  }
}
```
result would be something like
```json
{
  "data": {
    "contacts": [
      {
        "firstname": "Cody",
        "email": "traciroberts@booth.com"
      },
      {
        "firstname": "Lisa",
        "email": "mcabrera@hall.net"
      },
      {
        "firstname": "Samantha",
        "email": "smithchelsea@woods-cook.com"
      },
      {
        "firstname": "Darrell",
        "email": "vincentbrenda@gmail.com"
      },
      {
        "firstname": "Jeremy",
        "email": "marissathomas@hotmail.com"
      },
      {
        "firstname": "Linda",
        "email": "wolfeemily@mcguire.net"
      },
      {
        "firstname": "Judy",
        "email": "armstrongsylvia@hubbard-molina.net"
      },
      {
        "firstname": "Emily",
        "email": "benjaminanderson@hardy.com"
      },
      {
        "firstname": "Mark",
        "email": "miguelwilliams@thompson.com"
      },
      {
        "firstname": "Darryl",
        "email": "ebenson@gmail.com"
      }
    ]
  }
}
```
or something bit complex like
```
query allContacts{

  companies {
    name
  }
  telephones {
    number,
    contact {
      firstname,
      email,
      projects {
        name
      	tasks{
          title
        }
      }
    }
  }
  
}
```
result would be something like
```json
{
  "data": {
    "companies": [
      {
        "name": "Johnson Inc"
      },
      {
        "name": "Brown-Johnston"
      },
      {
        "name": "Rodgers, Keller and Leblanc"
      },
      {
        "name": "Chavez Group"
      },
      {
        "name": "Beck, Hubbard and Mcdaniel"
      }
    ],
    "telephones": [
      {
        "number": "1-173-159-3045",
        "contact": {
          "firstname": "Cody",
          "email": "traciroberts@booth.com",
          "projects": []
        }
      },
      {
        "number": "1-924-690-7634x10346",
        "contact": {
          "firstname": "Lisa",
          "email": "mcabrera@hall.net",
          "projects": []
        }
      },
      {
        "number": "(522)626-1798",
        "contact": null
      },
      {
        "number": "1-760-337-8278",
        "contact": {
          "firstname": "Samantha",
          "email": "smithchelsea@woods-cook.com",
          "projects": []
        }
      },
      {
        "number": "+75(0)9779901738",
        "contact": {
          "firstname": "Darrell",
          "email": "vincentbrenda@gmail.com",
          "projects": []
        }
      },
      {
        "number": "03509440288",
        "contact": null
      },
      {
        "number": "+80(5)9904302486",
        "contact": {
          "firstname": "Jeremy",
          "email": "marissathomas@hotmail.com",
          "projects": []
        }
      },
      {
        "number": "1-227-232-6160",
        "contact": {
          "firstname": "Linda",
          "email": "wolfeemily@mcguire.net",
          "projects": []
        }
      },
      {
        "number": "(265)126-3837x9009",
        "contact": null
      },
      {
        "number": "684-922-2803",
        "contact": {
          "firstname": "Judy",
          "email": "armstrongsylvia@hubbard-molina.net",
          "projects": []
        }
      },
      {
        "number": "(675)862-4392x0051",
        "contact": {
          "firstname": "Emily",
          "email": "benjaminanderson@hardy.com",
          "projects": []
        }
      },
      {
        "number": "1-245-519-4472x16616",
        "contact": null
      },
      {
        "number": "(739)930-3276x829",
        "contact": {
          "firstname": "Mark",
          "email": "miguelwilliams@thompson.com",
          "projects": []
        }
      },
      {
        "number": "+06(4)0572394046",
        "contact": {
          "firstname": "Darryl",
          "email": "ebenson@gmail.com",
          "projects": []
        }
      },
      {
        "number": "+86(3)3383213410",
        "contact": null
      }
    ]
  }
}
```
### example
Simple examples using gql  https://github.com/graphql-python/gql 
```ipython
In [31]: from gql import gql, Client
```

querying all contacts
```ipython
In [32]: query = """query allContacts {
    ...: contacts { 
    ...:   firstname, 
    ...:   email
    ...:   }
    ...: }"""

In [33]: from gql.transport.requests import RequestsHTTPTransport

In [34]: transport = RequestsHTTPTransport("http://localhost:5000/graphql")

In [35]: cl = Client(transport=transport)

In [36]: cl.execute(gql(query))
Out[36]: 
{'contacts': [{'email': 'traciroberts@booth.com', 'firstname': 'Cody'},
  {'email': 'mcabrera@hall.net', 'firstname': 'Lisa'},
  {'email': 'smithchelsea@woods-cook.com', 'firstname': 'Samantha'},
  {'email': 'vincentbrenda@gmail.com', 'firstname': 'Darrell'},
  {'email': 'marissathomas@hotmail.com', 'firstname': 'Jeremy'},
  {'email': 'wolfeemily@mcguire.net', 'firstname': 'Linda'},
  {'email': 'armstrongsylvia@hubbard-molina.net', 'firstname': 'Judy'},
  {'email': 'benjaminanderson@hardy.com', 'firstname': 'Emily'},
  {'email': 'miguelwilliams@thompson.com', 'firstname': 'Mark'},
  {'email': 'ebenson@gmail.com', 'firstname': 'Darryl'}]}


```
querying all phone numbers.
```ipython
In [37]: query2 = """query phones {
    ...:     telephones {
    ...:        number 
    ...:     }
    ...: }"""
In [38]: cl.execute(gql(query2))
Out[38]: 
{'telephones': [{'number': '1-173-159-3045'},
  {'number': '1-924-690-7634x10346'},
  {'number': '(522)626-1798'},
  {'number': '1-760-337-8278'},
  {'number': '+75(0)9779901738'},
  {'number': '03509440288'},
  {'number': '+80(5)9904302486'},
  {'number': '1-227-232-6160'},
  {'number': '(265)126-3837x9009'},
  {'number': '684-922-2803'},
  {'number': '(675)862-4392x0051'},
  {'number': '1-245-519-4472x16616'},
  {'number': '(739)930-3276x829'},
  {'number': '+06(4)0572394046'},
  {'number': '+86(3)3383213410'}]}

```

## Development
- Models are defined as SQLAlchemy models in`models.py` file, and the specs are here https://github.com/Incubaid/crm/blob/master/model.md

- Fixtures to be included in fixtures.py
- To register a model in `Flask-Admin`: add it to `dbmodels` list and it'll be autoregisted in the admin



