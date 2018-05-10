# [CouchDB](https://hub.docker.com/_/couchdb/)
[Official docs](http://docs.couchdb.org/en/2.1.0/)

docker run --name iCouchdb -p 5984:5984 -v ~/my_directory/local.d:/opt/couchdb/etc/local.d -e COUCHDB_USER=cluster12 -e COUCHDB_PASSWORD=cluster12 -d couchdb
## How to use docker image
	docker pull couchdb
### Start a CouchDB instance
	$ docker run -d --name my-couchdb couchdb
### Using the instance
In order to use the running instance from an application, link the container

	$ docker run --name my-couchdb-app --link my-couchdb:couch couchdb
### Exposing the port to the outside world
WARNING: Do this until admin user has been established and permissions has been setup correctly!

	$ docker run -p 5984:5984 -d couchdb
## Persistent Data
CouchDB uses /opt/couchdb/data to store its data, and is exposed as a volume.  
CouchDB uses /opt/couchdb/etc to store its configuration.

### Using host directories
	$ docker run -d -v $(pwd):/opt/couchdb/data --name my-couchdb couchdb

## Specifying the admin in the environment
	$ docker run -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -d couchdb

## Using your own CouchDB configuration file
The CouchDB configuration is specified in .ini files in /opt/couchdb/etc.  
	$ docker run --name my-couchdb -v /my/custom-config-dir:/opt/couchdb/etc/local.d -d couchdb

### Example Dockerfile
	FROM couchdb
	COPY local.ini /opt/couchdb/etc/

and then build and run

	$ docker build -t you/awesome-couchdb .
	$ docker run -d -p 5984:5984 you/awesome-couchdb

## Logging
By default containers run from this image only log to stdout. You can enable logging to file in the configuration.  
For example in local.ini:

	[log]
	writer = file
	file = /opt/couchdb/log/couch.log
