# Room-App

This is an app to chat in real-time in different rooms using Django mainly. It's main features are:

- Real time chat using WebScokets
- User registration, login and logout
- Implementation of API's with logging include
- Caching using Redis

### requirments
- docker
- docker-compose

### Instalation steps
> if you have a newer version of docker-compose replace `docker-compose` with `docker compose` in the following steps
-  clone this repository: `git clone https://github.com/urielmayo/room-app.git` or  `git clone git@github.com:urielmayo/room-app.git`
-  Create an `.env` file including this keys and fill the fields in <>:
```
SECRET_KEY=<your_secret_key> # You can use tool like djecretkey
POSTGRES_DB=<db_name>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
- build the containers: `docker-compose build`
- Start the servers: `docker-compose up`

You should be done by now.
Open http://0.0.0.0:8000/ on your browser, signup and start chatting!.


To run tests for a special app, run the following command:
`docker-compose run --rm --service-ports django python manage.py test apps.<app_name>`