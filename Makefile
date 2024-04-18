run-server:
	python manage.py runserver
migrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
admin:
	python manage.py createsuperuser
collectstatic:
	python manage.py collectstatic
freeze:
  pip freeze > requirements.txt
# createapp: # + appname
#     python manage.py startapp $(appname)
#     @echo "App $(appname) created successfully."
