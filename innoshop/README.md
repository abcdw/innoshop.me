You can use virtualenv to store packages for each project separately.
Add `--user` to `pip install` command if you don't use virtualenv

```
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```


For loading fixtures of db
```
./manage.py loaddata 
```
