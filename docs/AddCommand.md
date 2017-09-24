## AddCommand

- open ```cli.py```
- add your command function with a docorator by ```@app.cli.command()```
- Example
    ```python
    @app.cli.command()
    def loadfixtures():
        generate_fixtures()
    ```
