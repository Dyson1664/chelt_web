set -o errexit

pip install -r requirements.txt

pip manage.py collectstatic --noinput
python manage.py migrate

