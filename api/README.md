# Peeple API

Exposes a REST API for all the functionalities required by the front-end client.

### Installing all the dependancies

```sh
cd api
pip3 install -r requirements.txt
```
### Setting up the database

```sh
FLASK_APP=main flask db init
FLASK_APP=main flask db migrate -m "New Tables"
FLASK_APP=main flask db upgrade
```
### Starting the server

```sh
python3 main.py
```
### Endpoints

- `GET /peep`: Peep functionality

- `POST /sign_up`: Creates new user

- `GET /user_list` : Fetches existing user list

- `POST /users/{id}`: Updates existing user
