# CMPUT404_PROJECT

CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

## Installing Backend Dependencies
Note: Make sure to have python 3.6 or newer installed

Go into a terminal window in the root directory of this repository and run  
```
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

// Then get a .env file from one of the project members
and put it in the same directory as `manage.py`
```

## Helpful Backend Commands

If PostgreSQL is running, 
`python3 manage.py runserver`  to startup the server.

To create an admin user: `python3 manage.py createsuperuser`. 

Saving new python dependencies: `pip freeze > requirements.txt`.

## Installing DB
Make sure you have install the required Python packages first above.
The following commands are to be run within a virtual env.

Note: This is done on OSX
```
brew install postgresql

// To start PostgreSQL
brew services start postgresql

// To stop PostgreSQL
brew services stop postgresql

// To use the CLI
createuser -s postgres 
psql postgres

Then within the shell run any commands such as...
CREATE DATABASE myproject;
ALTER ROLE myprojectuser SET client_encoding TO 'utf8'; etc.

\q to quit
```

If you're making any DB changes, make sure PostgreSQL has started then
```
python3 manage.py makemigrations
python3 manage.py migrate
```


Repo Contributors / Licensing
=============================

Team Members:

    Kean Weng Yap
    Monica Bui
    Ian Seng Wok
    Amy Xiang
    Hailan Xu

Project Creation Contributors / Licensing
========================

LICENSE, README.md and project.org files are inherited [Professor Abram Hindle's repo](https://github.com/abramhindle/CMPUT404-project-socialdistribution).

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma


References
=============================
Connecting PostgreSQL to Django
* From [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
* From [Justin Ellingwood](https://www.digitalocean.com/community/users/jellingwood)
* Accessed Feb 9 2021


Adding secrets to env file
* From [StackOverflow](https://stackoverflow.com/a/61437799)
* From [Zack Plauché](https://stackoverflow.com/users/10415970/zack-plauch%c3%a9)
* Accessed Feb 9 2021

Adding PostgreSQL to GitHub Actions Job
* From [HackSoft](https://hacksoft.io/github-actions-in-action-setting-up-django-and-postgres/)
* From [Radoslav Georgiev](https://hacksoft.io/author/radoslav-georgiev/)
* Accessed Feb 9 2021

UUID Django Model Field Type
* From [Django Docs](https://docs.djangoproject.com/en/3.1/ref/models/fields/#uuidfield)
* Accessed Feb 13 2021