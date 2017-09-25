## AddCommand

- open ```cli.py```
- surround your command function with a docorator ```@app.cli.command()```
- Example
    ```python
    @app.cli.command()
    def loadfixtures():
        generate_fixtures()
    ```
