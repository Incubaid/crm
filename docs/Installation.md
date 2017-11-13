# Installation

- CRM is a [Flask](flask.pocoo.org/) app
- We have 2 main modes to install and run the application ```Development``` & ```Production``` modes
Depending on the mode you're running requirements may change (a bit) not dramatically

### Prepare Your virtual environment

- ```virtualenv -p python3 crm_env```
- ```. crm_env/bin/activate```


### Install required packages

###### Automatically

- Use the script ```./prepare.sh``` to install all dependencies
- usage:
    ```
    ./prepare --prod (Install Production dependencies)
    ./prepare --dev (Install Development dependencies)
    ```

###### Manually

- Install System level dependencies
    - Ubuntu ```apt-get -y < requirements.apt```
    - Mac ```xargs brew install < requirements.brew```

- Install Python level dependencies
    - Development environment ```pip3 install -r requirements-testing.pip```
    - Production environment  ```pip3 install -r requirements.pip```

- Install Nodejs level dependencies
    - Development environment ```cat requirements.npm | sudo xargs npm install -g```
    - Production environment ```Nothing yet```

### Notes

- Development mode python packages that are not needed in production:
    - ```flask-shell-ipython```
    - ```coverage```
    - ```nose```
    - ```ipdb```

- Development nodejs packages that are not needed in production:
    - ```@2fd/graphdoc``` It's used to re-create graphql API docs from a [graphql](http://graphql.org/learn/) schema file and it's the only
    nodejs dependency for now
