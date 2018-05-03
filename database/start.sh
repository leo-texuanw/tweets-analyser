# -d: run in detached mode
# outer_port:docker_port
sudo docker run -d -p 5984:5984 --env COUCHDB_USER=cluster --env COUCHDB_PASSWORD=cluster12 --volume /database:/opt/couchdb/data --volume /database/local.d:/opt/couchdb/etc/local.d --name couchdb-cluster couchdb

# add node in cli:
#     exec `docker exec -it couchdb bash` to enter
