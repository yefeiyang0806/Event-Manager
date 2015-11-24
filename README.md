# Event-Manager

## Environment:
* Python 3.4
* MySQL 5.7.9 (database: event_manager, username: root, password:rootadmin)
* PyMySQL3-0.5
* Flask-login/mail/SQLAlchemy/wtf/bootstrap

##Instructions:
*(Please remove the flask folder and rebuild the whole virtual environment to make sure the application can run properly. The new environment folder should be named as "flask" and then install flask, flask-mail, flask-sqlalchemy, flask-login, flask-wtf, flask-bootstrap and sqlalchemy-migrate)
* 1. Activate virtualenv from EventManager/flask/Scripts/activate
* 2. Create an empty database in MySQL named event_manager, and add user with the provided username and password.
* 3. Create the database by python EventManager/db_create.py
* 4. Start the app by python Eventmanager/run.py

##Current Features:
* Register and log in an account.
* Passwords are hashed and UUID is used as the primary key.
* Send a confirmation email to the registered email address.
* Activate the account (the link hasn't been deployed in the template yet. The activation could be done manually by typing http://localhost:5000/activate_user?active_code={{active_code in db}}.)
* Users can register new events, do modification and deletion on  their created events.

##Following targets:
* Design and adapt blueprints
* Add a password forgot feature
* TBD
