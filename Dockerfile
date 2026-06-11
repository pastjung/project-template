FROM mysql:8.4

COPY conf.d/my.cnf /etc/mysql/conf.d/my.cnf
COPY initdb/ /docker-entrypoint-initdb.d/
