from setuptools import setup

setup(
    name='crm',
    packages=['crm'],
    include_package_data=True,
    install_requires=[
        'flask',
        'uwsgi',
    ],
)
