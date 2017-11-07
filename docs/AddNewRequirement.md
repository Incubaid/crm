## How to add new System requirement

**System requirements**

- Linux/Ubuntu : add it to `requiremtns.apt`
- Mac : add it to `requiremtns.brew`

**Python package**

- Add to `requiremtns.pip` & `requiremtns-testing.pip` using the following procedure
    - Create and activate new virtualenv `virtualenv -p python3 my_env` && `. my_env/bin/activate`
    - Install old requirements `pip install -r requiremtns.pip`
    - Save installed package in a file using `pip freeze > file1.txt` or using a tool like [pepreqs](https://github.com/bndr/pipreqs)
    - Install new packag(s)
    - Save installed package in a file using `pip freeze > file2.txt` or using a tool like [pepreqs](https://github.com/bndr/pipreqs)
    - Get difference between 2 files `diff file1.txt file2.txt`
    - Add difference package to `requirements.pip` & `requirements-testing.pip`

