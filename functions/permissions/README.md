# Permissions 🔒

Built-in permissions, ring-fencing function

EAMENA DB = 
test DB = http://34.244.135.144/

## Built-in permissions

Natively, Arches allows:

Arches Designer > Resource Model > Heritage Place > Permissions >   
    - [EAMENA](https://database.eamena.org/en/graph_designer/34cfe98e-c2c0-11ea-9026-02e7594ce0a0)
    - [test](http://34.244.135.144/graph_designer/34cfe98e-c2c0-11ea-9026-02e7594ce0a0)


## Ring-fencing function

Arches function to allow different user subgroups to access different resources

The function will only apply the rules on newly created resources.

To make the function work on pre-existing resrouces run the included `resave_all_resource` command.

### Installation

1. `.htm` 

place the `.htm` file in `template -> views -> components -> functions`

2. `.js`

placec the `.js` file in `media -> js -> views -> components -> functions`

3. `.py`

place the `.py` file in `functions`

4. Register function

finally register your function using the following command

```
python manage.py fn register --source '/path/to/function_name.py
```

5. Add a view

Place `userandgroups.py` in `project_name -> views`

6. Urls

In `urls.py` add the following import at the top of the page
```
from .views.userandgroups import getUsers
```
Finally add the following url pattern to at the top of the `urlpatterns` array
```
url(r"^get/users", getUsers.as_view(), name="getUsers"),
```

### Optional `resave_all_resrouces` command

Copy the `resave_all_resrouces` to 
```
your/arches/installtion/managment/commands/
```

and run the following 
```
python manage.py resave_all_resrouces
```

---

files

* [ringfencing.htm](https://github.com/eamena-oxford/eamena-arches-dev/blob/main/functions/ring-fencing/files/ringfencing.htm)
* [ringfencing.js](https://github.com/eamena-oxford/eamena-arches-dev/blob/main/functions/ring-fencing/files/ringfencing.js)
* [ringfencing.py](https://github.com/eamena-oxford/eamena-arches-dev/blob/main/functions/ring-fencing/files/ringfencing.py)
* [userandgroups.py](https://github.com/eamena-oxford/eamena-arches-dev/blob/main/functions/ring-fencing/files/userandgroups.py)
* [resave_all_resources.py](https://github.com/eamena-oxford/eamena-arches-dev/blob/main/functions/ring-fencing/files/resave_all_resources.py)

bash script for function installation

* [ringfencing.sh](https://github.com/eamena-oxford/eamena-arches-dev/tree/main/functions/ring-fencing/ringfencing.sh)

---

## Tests


User: test_permission
Pwd: *see Slack* 
