

run:
	docker-compose up --build;


start_db:
	docker-compose up postgresDB -d;


stop_db:
	docker-compose down postgresDB;


deploy:
	docker-compose up --build -d;


all_down:
	docker-compose down;


logs:
	docker-compose logs -f;