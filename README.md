## Installation
```
    virtualenv -p python3 crm_env
    . crm_env/bin/activate

    git clone https://github.com/Incubaid/crm
    cd crm/app
    pip3 install -r requirements.pip
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser   #provide username/pass for admin i.e (admin, a12345678)
```

## importing models Data
```
python3 manage.py loaddata contact/fixtures/*
python3 manage.py loaddata company/fixtures/*
python3 manage.py loaddata organization/fixtures/*
python3 manage.py loaddata project/fixtures/*
python3 manage.py loaddata sprint/fixtures/*
python3 manage.py loaddata deal/fixtures/*
python3 manage.py loaddata message/fixtures/*
python3 manage.py loaddata task/fixtures/*
python3 manage.py loaddata comment/fixtures/*
python3 manage.py loaddata link/fixtures/*
```

## Running

```
python manage.py runserver

open http://127.0.0.1/admin in your browser
```


## Exporting data (INDIVIDUAL MODELS)

- If you have changes in Database that you want to export into json
- you can export any model using ```python manage.py dumpdata app_name.model_name --format json --indent 4 > filename.json```

- examples:
    ```
    python3 manage.py dumpdata contact.contact --format json --indent 4 > contact/fixtures/contacts.json
    python3 manage.py dumpdata contact.ContactEmail --format json --indent 4 > contact/fixtures/emails.json
    python3 manage.py dumpdata contact.ContactPhone --format json --indent 4 > contact/fixtures/phones.json
    python3 manage.py dumpdata contact.MessageChannel --format json --indent 4 > contact/fixtures/messageChannels.json

    python3 manage.py dumpdata company.company --format json --indent 4 > company/fixtures/companies.json
    python3 manage.py dumpdata company.companyemail --format json --indent 4 > company/fixtures/emails.json
    python3 manage.py dumpdata company.companyphone --format json --indent 4 > company/fixtures/phones.json

    python3 manage.py dumpdata link.link --format json --indent 4 > link/fixtures/links.json
    python3 manage.py dumpdata link.linklabel --format json --indent 4 > link/fixtures/linklabels.json

    python3 manage.py dumpdata message.message --format json --indent 4 > message/fixtures/messages.json
    python3 manage.py dumpdata message.messagecontact --format json --indent 4 > message/fixtures/contacts.json

    python3 manage.py dumpdata task.task --format json --indent 4 > task/fixtures/task.json
    python3 manage.py dumpdata task.taskassignment --format json --indent 4 > task/fixtures/assignments.json
    python3 manage.py dumpdata task.tasktracking --format json --indent 4 > task/fixtures/trackings.json


    python3 manage.py dumpdata comment.comment --format json --indent 4 > comment/fixtures/comment.json

    python3 manage.py dumpdata deal.deal --format json --indent 4 > deal/fixtures/deal.json

    python3 manage.py dumpdata organization.organization --format json --indent 4 > organization/fixtures/organization.json
    python3 manage.py dumpdata project.project --format json --indent 4 > project/fixtures/project.json
    python3 manage.py dumpdata sprint.sprint --format json --indent 4 > sprint/fixtures/sprint.json
    ```

## Graphql Support
- Open ```http://127.0.0/graph```
- Insert query
    ```json
    {
      contact{
        firstName
        emails {
          id
        },
        deals {
          closedDate
        },
        comments{
          content
        }

      }
    }
    ```
    - Result should look like
    ```json

    {
      "data": {
        "contact": [
          {
            "firstName": "Hamdy",
            "emails": [
              {
                "id": "1"
              }
            ],
            "deals": [
              {
                "closedDate": "2017-09-03"
              }
            ],
            "comments": [
              {
                "content": "comment"
              }
            ]
          },
          {
            "firstName": "Peter",
            "emails": [
              {
                "id": "2"
              }
            ],
            "deals": [],
            "comments": []
          }
        ]
      }
    }
    ```
