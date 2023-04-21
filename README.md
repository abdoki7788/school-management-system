# Kharazmi School Management System
Rest API Backend of A School Management system for Kharazmi Festival

## installation

```
this project is deployed on:
    https://school-management-system.iran.liara.run/
so you can just use this and you dont need to install it
```

### frontend : [https://github.com/Blankevoort/ManageStudents](https://github.com/Blankevoort/ManageStudents/)

### requirements:
 - python
 - virtualenv
 - git

note: python in linux intalled by default
for install python in windows, go to https://www.python.org/ and download python and install it

then run this command for install virtualenv

``` pip install virtualenv ```

for clone this project run this command
``` git clone [https://github.com/abdoki7788/school-management-system.git ](https://github.com/abdoki7788/school-management-system)
cd school-management-system
```

create a virtual envirement and activate

### linux

```
virtualenv .venv
source .venv/bin/activate
```

### windows

```
python -m virtualenv .venv
.venv\scripts\activate.bat
```

then install dependencie packages from requirements.txt using this command:

``` pip install -r requirements.txt ```

and run this commands to run django server:

```
python manage.py migrate
python manage.py runserver
```

and go to http://127.0.0.1:8000 and use this api!
