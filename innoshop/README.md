You can use virtualenv to store packages for each project separately.
Add `--user` to `pip install` command if you don't use virtualenv

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata fixtures/*
./manage.py collectstatic
./manage.py runserver
```


