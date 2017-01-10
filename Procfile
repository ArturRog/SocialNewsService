web: python manage.py makemigrations
web: python manage.py migrate
web: gunicorn SocialNewsService.wsgi --log-file -
heroku ps:scale web=1