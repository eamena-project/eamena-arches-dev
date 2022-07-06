# The function

The function will only apply the rules on newly created resrouces.

To make the function work on pre-existing resrouces run the included `resave_all_resource` command.

# Installation

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

## Optional `resave_all_resrouces` command

Copy the `resave_all_resrouces` to 
```
your/arches/installtion/managment/commands/
```

and run the following 
```
python manage.py resave_all_resrouces
```