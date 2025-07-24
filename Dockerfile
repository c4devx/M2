# python para el contenedor Docker
FROM python:3.10

# dbt para PostgresSQL
RUN pip install dbt-postgres

# seteo dir de trabajo dentro del contenedor
WORKDIR /app   