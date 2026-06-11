FROM mongo:8.0

COPY initdb/ /docker-entrypoint-initdb.d/
