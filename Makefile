makemigrations:
	docker compose exec api python manage.py makemigrations

migrate:
	docker compose exec api python manage.py migrate

# createsuperuser:
# 	docker compose exec api python manage.py createsuperuser

loaddata:
	docker compose exec --user root api python manage.py loaddata ./fixture.json

dumpdata:
	docker compose run --user root --rm api python manage.py dumpdata -o fixture.json

up:
	docker compose up --build

down:
	docker compose down

db:
	docker compose exec db psql -U postgres -d recommendation
