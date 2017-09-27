## Middlewares

**What is a middleware**

- A middleware in a web application is a piece of software that runs
before any request in the web application and thus it can do operations
that is global to all/some http actions in your app

- Examples:
    - A middleware can handle authenticatin and check token headers, return 403 if usee is not autorized or 401 if not authenticated

**How to add a middleware in CRM system**

- Just add your middleware function in ```middlewares.py```
- surround your middleware function with ```@app.before_first_request```
