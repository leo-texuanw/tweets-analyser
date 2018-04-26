chmod +x configure.sh

docker build -t couchbase-custom .

sleep 5

docker run -d -p 8091-8093:8091-8093 -e COUCHBASE_ADMINISTRATOR_USERNAME=Administrator -e COUCHBASE_ADMINISTRATOR_PASSWORD=password -e COUCHBASE_BUCKET=default -e COUCHBASE_BUCKET_PASSWORD= --network="bridge" --name couchbase1 couchbase-custom
# docker run -d -p 8094-8096:8091-8093 -e COUCHBASE_ADMINISTRATOR_USERNAME=Administrator -e COUCHBASE_ADMINISTRATOR_PASSWORD=password -e COUCHBASE_BUCKET=default -e COUCHBASE_BUCKET_PASSWORD= --network="bridge" --name couchbase2 couchbase-custom
# docker run -d -p 8097-8099:8091-8093 -e COUCHBASE_ADMINISTRATOR_USERNAME=Administrator -e COUCHBASE_ADMINISTRATOR_PASSWORD=password -e COUCHBASE_BUCKET=default -e COUCHBASE_BUCKET_PASSWORD= --network="bridge" --name couchbase3 couchbase-custom

# Or add in cli:
#     exec `docker exec -it couchbase1 bash` to enter
# input:
#     /opt/couchbase/bin/couchbase-cli server-add --cluster=localhost:8091 --user Administrator --password password --server-add 172.17.0.3 --server-add-username Administrator --server-add-password password
