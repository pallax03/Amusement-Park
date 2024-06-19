FROM mysql:8.0

COPY ./init.sql /docker-entrypoint-initdb.d/
COPY ./populate.sql /docker-entrypoint-initdb.d/
RUN chmod -R 775 /docker-entrypoint-initdb.d