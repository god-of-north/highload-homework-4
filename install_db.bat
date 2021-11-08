git clone https://github.com/devrimgunduz/pagila.git
type create_db.sql | docker exec -i highload-homework-4_db_1 psql -U hello_flask postgres
type .\pagila\pagila-schema.sql | docker exec -i highload-homework-4_db_1 psql -U hello_flask pagila
type .\pagila\pagila-data.sql | docker exec -i highload-homework-4_db_1 psql -U hello_flask pagila
