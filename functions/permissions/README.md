# Permissions 🔒

bulk-application of instance-level permissions
Built-in permissions, ring-fencing function

EAMENA DB = 
test DB = http://34.244.135.144/

## Built-in permissions

Natively, Arches allows:

Arches Designer > Resource Model > Heritage Place > Permissions >   
    - [EAMENA](https://database.eamena.org/en/graph_designer/34cfe98e-c2c0-11ea-9026-02e7594ce0a0)
    - [test](http://34.244.135.144/graph_designer/34cfe98e-c2c0-11ea-9026-02e7594ce0a0)

### Card

* ~~solution 1~~
    - duplicate the `eamena-default-card`
    - rename the duplicate `eamena-permission-card`
(see https://community.archesproject.org/t/card-permission/1675?u=zoometh)
## Ring-fencing function

The RF function is a bulk-application of instance-level permissions created by Knowlegde Intergation and Farallon (Reuben Osborne) delivered to EAMENA-Oxford the 9th March 2022. Its aim is to allow different user subgroups to access different resources.

### Disclaimer

#### Function behaviour

According to KI and Farallon: *"If an instance has permissions on it, it is not added to the layer. The reason is that checking permissions on instance in the layer would be very expensive. I was in favor of doing it anyway, but others thought the performance hit would be too much. So it was decided just to hide the instances in the map."*

#### Affected resources

The function will only apply the rules on newly created resources. To make the function work on pre-existing resrouces run the included `resave_all_resource` command.

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
