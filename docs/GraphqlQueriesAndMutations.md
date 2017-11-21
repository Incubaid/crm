## Queries and Mutations

- We go through some General examples on making queries & Mutations.
- We use the ```Contact``` model as an example

#### Query API

- Queries

    - **Query ALL Data**
        - We use **```contacts```** query to get all contacts
        - You define what fields you want to see in result inside ```node```

             ```
                    {
                      contacts{
                        edges{
                          node{
                            firstname
                            lastname
                            uid
                          }
                        }
                      }
                    }
             ```
        - Result looks like
            ```
            {
                  "data": {
                    "contacts": {
                      "edges": [
                        {
                          "node": {
                            "firstname": "Scott",
                            "lastname": "Rodriguez",
                            "uid": "yvsnb"
                          }
                        },
                        {
                          "node": {
                            "firstname": "Kelsey",
                            "lastname": "Smith",
                            "uid": "vwchm"
                          }
                        }
                      ]
                     }
                    }
            ```

    -  **Query one Record**
        - We also have a query called **```contact```** to get you a certain contact based on ID
            ```
                {
                  contact(uid: "vwchm"){
                    firstname
                    lastname
                    uid
                  }
                }
            ```

        - and result looks like
            ```
            {
              "data": {
                "contact": {
                  "firstname": "Kelsey",
                  "lastname": "Smith",
                  "uid": "vwchm"
                }
            }
            }
            ```

    - **Pagination**
        - [More about Pagination](http://graphql.org/learn/pagination/) in graphql
        - You need to add to your query 2 more fields
            - cursor ```added to edges``` (record Internal ID) consider it as page number
            - pageInfo (Pagination footer) containing stuff like ```has next```, ```start``` and ```end```
            ```pageInfo{
                      hasNextPage
                      hasPreviousPage
                      startCursor
                      endCursor
               }
            ```
        - Example
            ```
            {
                  contacts{
                    edges{
                      node{
                        firstname
                        lastname
                        uid
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
        - result looks like
            ```
            {
              "data": {
                "contacts": {
                  "edges": [
                    {
                      "node": {
                        "firstname": "Scott",
                        "lastname": "Rodriguez",
                        "uid": "yvsnb"
                      },
                      "cursor": "YXJyYXljb25uZWN0aW9uOjA="
                    },
                        ...
                  ]

                  "pageInfo": {
                        "hasNextPage": false,
                        "hasPreviousPage": false,
                        "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
                        "endCursor": "YXJyYXljb25uZWN0aW9uOjM4"
                  }
                 }
               }
            }
            ```
        - Then you can get whatever subset of data like
            ```
            {
                  contacts(first:1, after: "YXJyYXljb25uZWN0aW9uOjA="){
                    edges{
                      node{
                        firstname
                        lastname
                        uid
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
    - **Filtration**
        - We use [Special Query syntax](GraphqlQueryLanguage.md) for querying data as
        - You can nest your queries as indicated in this example

        - Example
            ```
            {
              contacts(firstname: "hamdy", tasks: {title: "contains(hamdy_task)"}){
                edges{
                  node{
                    firstname
                    tasks{
                      edges{
                        node{
                          title
                        }
                      }
                    }
                  }
                }
              }
            }
            ```
        - Result
            ```
            {
              "data": {
                "contacts": {
                  "edges": [
                    {
                      "node": {
                        "firstname": "hamdy",
                        "tasks": {
                          "edges": [
                            {
                              "node": {
                                "title": "hamdy_task_1"
                              }
                            }
                          ]
                        }
                      }
                    }
                  ]
                }
              }
            }

            ```

        - Example(2)
            ```
            {
              deals(value: "600"){
                edges{
                  node{
                    name
                    value
                  }
                }
              }
            }
            ```
        - Result
            ```
            {
              "data": {
                "deals": {
                  "edges": [
                    {
                      "node": {
                        "name": "Ahmed Thabet",
                        "value": 600
                      }
                    },
                    {
                      "node": {
                        "name": "Hamdy Farag,
                        "value": 600
                      }
                    },
                    {
                      "node": {
                        "name": "Cutie boy",
                        "value": 600
                      }
                    },
                    {
                      "node": {
                        "name": "Pretty Girl",
                        "value": 600
                      }
                    },
                    ...
                  ]
                 }
                }
              }
            ```
    - You can query data using operators like `like()`, `contains()`, .. More info @[GraphQl API Query language](GraphqlQueryLanguage.md)
    - You can use queries like ```contacts(last:10)```, also u could use ```contacts(first:1, before: "YXJyYXljb25uZWN0aW9uOjA=")```


#### Mutations API

- Mutations

    - **create contact(s)**

        - in body of the mutation below you get back the ids of created objects
        - ok is boolean means success of failure

        - Example
        ```
        mutation{
            createContacts(records: [{firstname: "john", emails:"a@s.com", telephones: "01228934568"}, {firstname: "peter", emails:"b2e@.com", telephones: "01228934562"}]){
                ok
                ids
            }
        }
        ```
        - Result looks like
            ```
            {
              "data": {
                "createContacts": {
                  "ok": true,
                  "ids": [
                    "d7y2t",
                    "g30ty"
                  ]
                }
              }
            }
            ```
    - **delete contact(s)**
        - We do delete objects if uids are found, otherwise we ignore, we don't check if uids exist or not
        - Example
        ```

        mutation{
          deleteContacts(uids: ["id1", "id2", "id3"]) {
            contact {
              id
            }
            ok
          }
        }
        ```

    - **Update contact(s)**
        - Example
        ```
        mutation{
          updateContacts(records: [{uid: "d7y2t", firstname: "BigJohn"}, {uid: "g30ty", firstname: "BigPeter"}]){
            ok

          }
        }
        ```
        - Result looks like
          ```
            {
              "data": {
                "updateContacts": {
                  "ok": true,
                  "ids": [
                    "d7y2t",
                    "g30ty"
                  ]
                }
              }
            }
          ```
