#Collect static files

docker-compose exec web python manage.py collectstatic --no-input --clear

#Migrate

docker-compose exec web python manage.py migrate

#Delete old links

docker-compose exec web python manage.py delete_old_links

