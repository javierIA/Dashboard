sudo docker run --interactive --tty --rm --volume=$(pwd)/neo4j/data:/data  --volume=$(pwd)/neo4j/backups:/backups  neo4j/neo4j-admin:5.4.0 neo4j-admin database load neo4j --from-path=/backups --overwrite-destination

