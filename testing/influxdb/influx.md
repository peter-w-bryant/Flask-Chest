docker run --tty --interactive --rm --net host \
    --env DOCKER_INFLUXDB_INIT_MODE="setup" \
    --env DOCKER_INFLUXDB_INIT_ORG="my-org" \
    --env DOCKER_INFLUXDB_INIT_BUCKET="my-bucket" \
    --env DOCKER_INFLUXDB_INIT_USERNAME="my-user" \
    --env DOCKER_INFLUXDB_INIT_PASSWORD="my-password" \
    --env DOCKER_INFLUXDB_INIT_ADMIN_TOKEN="my-token" \
    --name influxdb-2.x \
    influxdb:latest