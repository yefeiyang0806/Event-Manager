# Event-Manager

## Environment:
* Python 3.4
* MySQL 5.7.9 (database: event_manager, username: root, password:rootadmin)
* PyMySQL3-0.5
* Flask-login/mail/SQLAlchemy/wtf/bootstrap

##Instructions:
*(Please remove the flask folder and rebuild the whole virtual environment to make sure the application can run properly. The new environment folder should be named as "flask" and then install flask, flask-mail, flask-sqlalchemy, flask-login, flask-wtf, flask-bootstrap and sqlalchemy-migrate)
* 1. Create a virtual environment with python 3.4 and install all the packages listed in /EventManager/requirements.txt via pip.
* 2. Create an empty database in MySQL named event_manager, and add user with the provided username and password.
* 3. Activate the virtualenv and create the database by "python EventManager/db_create.py"
* 4. Start the app by "python Eventmanager/run.py"
* 5. Direct the web-browser to url '/generate_db' to insert several essential records in db.
* 6. Register a new account, and after logged in, redirect to '/generate_resource' to insert several records for Resource.

##Current Features:
* Register and log in an account.
* Retrieve forgotten password via email address.
* Send a confirmation email to the registered email address.
* Activate the account through the activation code sent in the confirmation email.
* Users can register new topics, do modification and deletion on  their created topics.
* By this stage, all created users would have permission to see the menu of Role Mgmt and Topic Mgmt on the side bar.
* Through the Role Management, users can create roles.
* Through the Topic Management, users can validate topics and schedule topics.

##Following targets:
* Features of Role Mgmt should be riched (such as assigning a certain role to a certain user)
* Management of resource, resource type, content, format, menu are nmissing now
 