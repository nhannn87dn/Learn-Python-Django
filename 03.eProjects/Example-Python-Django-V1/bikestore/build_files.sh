echo "BUILD START"
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
python manage.py migrate
echo "BUILD END"