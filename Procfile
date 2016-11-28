web:python manage.py runserver
web: gunicorn SocialNewsService.wsgi --log-file -
heroku ps:scale web=1