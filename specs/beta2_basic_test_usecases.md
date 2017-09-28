
## what

describe some use cases for testing our beta2

## test 1

- add task to user/contact/deal/project/sprint/company
- be able to assign 1 user to a task (from user table)
- make sure this task is visible in details view
- make sure we can query the task from task filter list

## test 2

- make sure user can see his assigned tasks & filter on user/contact/deal/project/sprint/company (linked to task)
- this needs to be easy for a user

## test 3

- everyone logs in over IYO, each modified object needs to show author (original & modified) so we know who changed & when
- this needs to be visible in each object in detail mode

## test 4

- test messages, comments & links to user/contact/deal/project/sprint/company
- in detail view on comments we need to see author & moddate (so in relation to last change)

## test 5

- export all data
- in each json there needs to be subobj: tasks, messages, links, comments
- remove the DB
- import all data back 
- crm needs to have all data

## test 6

- create python script which on server works with the flask objects & does some manipulations against postgresql

## test 10

- create a python test program, is linked to a subgroup which has rights to crm
- from this test program do a graphql query 

