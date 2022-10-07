# ReaderHub

## Dependencies

- psycopg2>=2.8
- asgiref==3.2.10
- Django==3.0.9
- sqlparse==0.2.4
- pillow == 7.0.0
- requests == 2.22.0

## Running Django project locally

- Run migrations using `python manage.py migrate`
- Run server using `python manage.py runserver`
- The server will run at `http://127.0.0.1:8000/` (default)

## Running with Docker Compose (PREFERRED)

- Re-build the image(s) using `docker-compose build` if any changes have been made to dependencies or the docker files
- Use command `docker-compose up` to run containers
- The server will run at `http://localhost:8000/` (default)
- To close the containers, either use `docker-compose down` in another terminal or interrupt using `CTRL + C`

NOTE: Replace `python` with `python3` if needed
