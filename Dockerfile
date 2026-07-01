FROM postgres:16

COPY conf.d/postgresql.conf /etc/postgresql/postgresql.conf
COPY initdb/ /docker-entrypoint-initdb.d/
