

- when delete/change/new for a data object
- put in redis
    - hset: $nameofobj(table):$uid -> value: the toml which is the dataobj
    - queue: 
      - msgpack list:
          - user_name
          - user_email
          - nameofobj e.g. task
          - uid
          - epoch
      - so we know what to process from hset
- a separate python process will
    - write data to git structure & commit with username
