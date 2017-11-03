# Caching

- We use [Flask Cache](https://pythonhosted.org/Flask-Cache/)
- For now We've 2 Types of supported cache backends
    - Memory
    - [Redis](https://redis.io/)

    > we can always add more backends easily since [Flask Cache](https://pythonhosted.org/Flask-Cache/) supports many other backends

- In development mode `memory` cache is used unless you explicitly do on of the following
    - Set `CACHE_BACKEND_URI` environment variable i.e `export CACHE_BACKEND_URI=redis://{ip}:{port}/{db_number}`
    - Changed the CACHE_BACKEND_URI setting in `crm.settings_dev.py` explicitly to refer to a[Redis](https://redis.io/) URL

- In production mode, You **must use `Redis`** by executing : ``export CACHE_BACKEND_URI=redis://{ip}:{port}/{db_number}``

**Problems with Memory Cache**

All will work fine but some commands like `flask dumpcache` won't work.
becasue cached memory in CRM app can't be accessed by another process run by another command `flask dumpcache`
If you're testing `flask dumpcache` or similar command, consider use a [Redis](https://redis.io/) cache
