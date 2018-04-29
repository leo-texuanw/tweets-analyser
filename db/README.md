# DB
our ip address: 43.240.97.107
our port: 5984

## Start server
    $ ./start
    $ export SERVER=http://name:password@ipAddress:port/

## Operations
### get all databases
    $ curl -X GET $SERVER/_all_dbs
    ["_global_changes","_replicator","_users"]
### create a new database
    $ curl -X PUT $SERVER/new_db_name
    {"ok":true}
### Insert a new doc
    $ curl -X GET $SERVER/_uuids
    {"uuids":["e716115e41e20c7af043920cf8003017"]}

    $ curl -X PUT $SERVER/test/e716115e41e20c7af043920cf8003017 -d "{\"a\":\"json objects\"}"
    {"ok":true,"id":"e716115e41e20c7af043920cf8003017","rev":"1-39c8b9f2f49b435e4315f275cfe08008"}
