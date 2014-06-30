# Solar Power Prediction System

## Project Dependencies
* Flask
  - `pip install flask`
* Flask-SQLAlchemy
  - `pip install flask-sqlalchemy`
* PostgreSQL server
  - Installation is OS dependant
* PostgreSQL-server-dev-x.x
  - Installation is OS dependant `sudo apt-get install postgresql-server-dev-9.1` for Ubuntu/Mint
* pyowm
  - `pip install pyowm`
* configparser
  - Probably installed by default
  - `pip install configparser`
* psycopg2
  - `pip install psycopg2`

## Project Installation
1. Clone the repo onto your computer:
  - `git clone https://github.com/cruncher19/Ubicomp-GPP`
2. Create a user and database in postgres for the prediction system to use
  - in my case I used user: greenhouse, database: greenhousePower
  - don't forget to give your user permissions on your new database
3. Change the `db_uri: db_uri: postgresql://greenhouse@localhost/greenhousePower` setting in the config file to point to your postgres instance
  - should be of the form: `db_uri: postgresql://<username>@localhost/<database>`
4. Run `python initdb.py` to initialize the postgres database
5. Call `python routes.py` to start the server
6. You're good to go!


## REST API Usage
You can store power information in the database by POSTing to the server like this:
`http://localhost:5000/storePowerProduction?powerLevel=50`

