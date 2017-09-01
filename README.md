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
    python manage.py runserver
```

## Running
``` open http://127.0.0.1/admin``` in your browser
