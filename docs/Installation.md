## Installation

**Required packages**
```
sudo apt-get install python3-dev libffi-dev

```

**Installation**
```
    virtualenv -p python3 crm_env
    . crm_env/bin/activate
    pip3 install -r requirements.pip
    export FLASK_APP=app.py
    flask run

```