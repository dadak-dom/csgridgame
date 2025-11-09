FROM mysql:latest

WORKDIR /db

COPY exported_db.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

