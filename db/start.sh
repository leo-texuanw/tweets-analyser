sudo docker run -d -p 5984:5984 --env COUCHDB_USER=cluster --env COUCHDB_PASSWORD=cluster12 --volume ~/data:/opt/couchdb/data --name couchdb-cluster couchdb
#--volume ~/etc/local.d:/opt/couchdb/etc/local.d

# add node in cli:
#     exec `docker exec -it couchdb bash` to enter
