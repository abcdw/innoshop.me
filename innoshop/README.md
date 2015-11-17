You can use virtualenv to store packages for each project separately.
Add `--user` to `pip install` command if you don't use virtualenv

Install virtualenv:
> pip install virtualenv

Create virtualenv:
> cd ~/envs
> virtualenv innoshop

Activate virtualenv:
> cd ~/envs
> source bin/activate


```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata fixtures/*
./manage.py collectstatic
./manage.py update_categories
./manage.py runserver
```


```
./manage.py maintenance on
./manage.py maintenance off
```
