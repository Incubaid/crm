## API operations on contacts

- **List all**
    - Query
        ```json
            {
              contacts{
                edges{
                  node{
                    uid
                    firstName
                  }

                }
              }
            }
        ```
    - Result
        ```json
        {
          "data": {
            "contacts": {
              "edges": [
                {
                  "node": {
                    "uid": "0ae6",
                    "firstName": "Hamdy"
                  }
                },
                {
                  "node": {
                    "uid": "714c",
                    "firstName": "Peter"
                  }
                }
              ]
            }
          }
        }

        ```

- **Pagination support**
    - (cursor) is the same as field (id) which is base64(model_name:uid)
    - We use cursor/id during pagination; i.e conacts(after:some_id)
    - For more info about pagination in Graphql, [click here](http://graphql.org/learn/pagination/)
    - Query (1)
        ```json
        {
          contacts{
            edges{
              node{
                uid
                firstName
              }
              cursor

            }
            pageInfo{
              hasNextPage
              hasPreviousPage
              startCursor
              endCursor
            }
          }
        }
        ```
    - Result (1)
        ```json
        {
          "data": {
            "contacts": {
              "edges": [
                {
                  "node": {
                    "uid": "0ae6",
                    "firstName": "Hamdy"
                  },
                  "cursor": "YXJyYXljb25uZWN0aW9uOjA="
                },
                {
                  "node": {
                    "uid": "714c",
                    "firstName": "Peter"
                  },
                  "cursor": "YXJyYXljb25uZWN0aW9uOjE="
                }
              ],
              "pageInfo": {
                "hasNextPage": false,
                "hasPreviousPage": false,
                "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
                "endCursor": "YXJyYXljb25uZWN0aW9uOjE="
              }
            }
          }
        }
        ```

    - Query (2)
        ```json
        {
          contacts(first:1, after: "YXJyYXljb25uZWN0aW9uOjA="){
            edges{
              node{
                uid
                firstName
              }
              cursor

            }
            pageInfo{
              hasNextPage
              hasPreviousPage
              startCursor
              endCursor
            }
          }
        }
        ```

    - Result (2)
        ```json
        {
          "data": {
            "contacts": {
              "edges": [
                {
                  "node": {
                    "uid": "714c",
                    "firstName": "Peter"
                  },
                  "cursor": "YXJyYXljb25uZWN0aW9uOjE="
                }
              ],
              "pageInfo": {
                "hasNextPage": false,
                "hasPreviousPage": false,
                "startCursor": "YXJyYXljb25uZWN0aW9uOjE=",
                "endCursor": "YXJyYXljb25uZWN0aW9uOjE="
              }
            }
          }
        }
        ```

- **Filteration**
    - using field_name in filteration means match (exact)
    - If you have a contact with ```first_name="Hamdy"``` and you used something like
    ```contacts(firstName: "hamdy")``` you get no results, in this case you can use:
    ```contacts(firstName_Iexact: "hamdy")``` which matches exact text case insensetive
    - You can filter by foreign key fileds like ```owner_FirstName_Iexact:blah```
    - You can filter by date ranges ```contacts(createdAt_Range: "2017-09-02, 2017-09-17")``` where start & end are non inclusive
    - Query (1)
        ```json
        {
          contacts(firstName: "hamdy"){
            edges{
              node{
                uid
                firstName
              }
              cursor

            }
            pageInfo{
              hasNextPage
              hasPreviousPage
              startCursor
              endCursor
            }
          }
        }
        ```
    - Result (1)
        ```json
        {
          "data": {
            "contacts": {
              "edges": [],
              "pageInfo": {
                "hasNextPage": false,
                "hasPreviousPage": false,
                "startCursor": null,
                "endCursor": null
              }
            }
          }
        }
        ```

    - Query (2)
        ```json
        {
          contacts(firstName_Iexact: "hamdy"){
            edges{
              node{
                uid
                firstName
              }
              cursor

            }
            pageInfo{
              hasNextPage
              hasPreviousPage
              startCursor
              endCursor
            }
          }
        }
        ```
    - Result (2)
        ```json
        {
          "data": {
            "contacts": {
              "edges": [
                {
                  "node": {
                    "uid": "0ae6",
                    "firstName": "Hamdy"
                  },
                  "cursor": "YXJyYXljb25uZWN0aW9uOjA="
                }
              ],
              "pageInfo": {
                "hasNextPage": false,
                "hasPreviousPage": false,
                "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
                "endCursor": "YXJyYXljb25uZWN0aW9uOjA="
              }
            }
          }
        }
        ```


- **Get By ID**
    - use contact(pk=uid); pk means PRIMARY KEY
    - Query

        ```json
        {
          contact(pk:"714c"){
            firstName
            uid
          }
        }
        ```
    - Result
    ```json
        {
          "data": {
            "contact": {
              "firstName": "Peter",
              "uid": "714c"
            }
          }
        }
    ```

- **Create new**
    - Mutation
        ```json
        mutation{
          createContact(firstName: "zeos", lastName: "God", emails:["a@s.com", "b@WE.COM"], phones:["123456789", "12349900"]){
            contact {
              uid
              id
              firstName
              lastName
              phoneNumbers{
                phone
              }
              emails{
                email
              }
            }
            ok
            errors
          }
        }
        ```
    - Result
    ```json
        {
          "data": {
            "createContact": {
              "contact": {
                "uid": "5372",
                "id": "Y29udGFjdDo1Mzcy",
                "firstName": "zeos",
                "lastName": "God",
                "phoneNumbers": [
                  {
                    "phone": "123456789"
                  },
                  {
                    "phone": "12349900"
                  }
                ],
                "emails": [
                  {
                    "email": "a@s.com"
                  },
                  {
                    "email": "b@WE.COM"
                  }
                ]
              },
              "ok": true,
              "errors": null
            }
          }
        }
        }
    ```

- **Update**
    - pk field is required
    - Mutation
        ```json
        mutation{
          updateContact(firstName: "zeos2", lastName: "God2", pk:"5372"){
            contact {
              uid
              id
              firstName
              lastName
              phoneNumbers{
                phone
              }
              emails{
                email
              }
            }
            ok
            errors
          }
        }
        ```
    - Result
    ```json
        {
          "data": {
            "updateContact": {
              "contact": {
                "uid": "5372",
                "id": "Y29udGFjdDo1Mzcy",
                "firstName": "zeos2",
                "lastName": "God2",
                "phoneNumbers": [
                  {
                    "phone": "123456789"
                  },
                  {
                    "phone": "12349900"
                  }
                ],
                "emails": [
                  {
                    "email": "a@s.com"
                  },
                  {
                    "email": "b@WE.COM"
                  }
                ]
              },
              "ok": true,
              "errors": null
            }
          }
        }
    ```

- **Delete**
    - Mutation (1)
        ```json
        mutation{
          deleteContact(pk:"5372"){
            ok
            errors
          }
        }
        ```
    - Result (1)
    ```json
        {
          "data": {
            "deleteContact": {
              "ok": true,
              "errors": null
            }
          }
        }
    ```
    - Mutation (2)
        ```json
        mutation{
          deleteContact(pk:"5372"){
            ok
            errors
          }
        }
        ```
    - Result (1)
    ```json
        {
          "data": {
            "deleteContact": {
              "ok": false,
              "errors": "{\"fields\": {}, \"code\": 404}",
              "contact": null
            }
          }
}
    ```
