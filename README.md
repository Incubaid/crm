## Installation
```
    virtualenv -p python3 crm_env
    . crm_env/bin/activate

    git clone https://github.com/Incubaid/crm
    cd crm/app
    pip3 install -r requirements.pip
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser   #provide username/pass for admin i.e (admin, a12345678)
```

## importing models Data
```
python manage.py loaddata contact/fixtures/*
python manage.py loaddata company/fixtures/*
python manage.py loaddata organization/fixtures/*
python manage.py loaddata project/fixtures/*
python manage.py loaddata sprint/fixtures/*
python manage.py loaddata deal/fixtures/*
python manage.py loaddata message/fixtures/*
python manage.py loaddata task/fixtures/*
python manage.py loaddata comment/fixtures/*
python manage.py loaddata link/fixtures/*
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
    python manage.py dumpdata contact.contact --format json --indent 4 > contact/fixtures/contacts.json
    python manage.py dumpdata contact.ContactEmail --format json --indent 4 > contact/fixtures/emails.json
    python manage.py dumpdata contact.ContactPhone --format json --indent 4 > contact/fixtures/phones.json
    python manage.py dumpdata contact.MessageChannel --format json --indent 4 > contact/fixtures/messageChannels.json

    python manage.py dumpdata company.company --format json --indent 4 > company/fixtures/companies.json
    python manage.py dumpdata company.companyemail --format json --indent 4 > company/fixtures/emails.json
    python manage.py dumpdata company.companyphone --format json --indent 4 > company/fixtures/phones.json

    python manage.py dumpdata link.link --format json --indent 4 > link/fixtures/links.json
    python manage.py dumpdata link.linklabel --format json --indent 4 > link/fixtures/linklabels.json

    python manage.py dumpdata message.message --format json --indent 4 > message/fixtures/messages.json
    python manage.py dumpdata message.messagecontact --format json --indent 4 > message/fixtures/contacts.json

    python manage.py dumpdata task.task --format json --indent 4 > task/fixtures/task.json
    python manage.py dumpdata task.taskassignment --format json --indent 4 > task/fixtures/assignments.json
    python manage.py dumpdata task.tasktracking --format json --indent 4 > task/fixtures/trackings.json


    python manage.py dumpdata comment.comment --format json --indent 4 > comment/fixtures/comment.json

    python manage.py dumpdata deal.deal --format json --indent 4 > deal/fixtures/deal.json

    python manage.py dumpdata organization.organization --format json --indent 4 > organization/fixtures/organization.json
    python manage.py dumpdata project.project --format json --indent 4 > project/fixtures/project.json
    python manage.py dumpdata sprint.sprint --format json --indent 4 > sprint/fixtures/sprint.json
    ```

