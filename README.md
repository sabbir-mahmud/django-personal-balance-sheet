# django-personal-balance-sheet
You can monitor your income and expenses details with this django application. you won't need to worry about change month or year details. this project can change date automatic. also you don't need to select month and years details.
# demo user on
<a href="https://moneybug-history.herokuapp.com" target="_blank">Moneybug-history</a>
* username: hyena
* password: Sm1213543525

# requirements 
* python 3.10
* django 4.0
* django-crispy-forms==1.13.0

# how to run:
* download or clone this repo
* python manage.py migrate
* python manage.py runserver [for localhost only]
* python manage.py runserver 0.0.0.0:8000 [for deploy this project on local network]

# create superuser
* python manage.py createsuperuser
* superuser required for run this application.

after creating superuser log on to django admin panel. create 12 month.
Now you can able to run this project, and monitor your expense and earning details.

