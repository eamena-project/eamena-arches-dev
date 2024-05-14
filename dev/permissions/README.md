# User Permissions
> Bulk-application of instance-level permissions, Built-in permissions, ...

## Aim

1. Hide HP coordinates for Guest users

## IT solution

### Built-in

Natively, Arches allows:

Arches Designer > Resource Model > Heritage Place > Permissions >   
    - [EAMENA](https://database.eamena.org/graph_designer/34cfe98e-c2c0-11ea-9026-02e7594ce0a0)

<p align="center">
  <img alt="img-name" src="image.png" width="700">
  <br>
</p>

### Custom

Duplicate EAMENA card, change the configuration of the duplicated card permissions in a way it can be seen by people in a particular group (user [permission level](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/users#eamena-new-groups))

- duplicate the `eamena-default-card`  
- rename the duplicate `eamena-permission-card`  

* see
	- the Card: https://github.com/search?q=repo%3Aeamena-project%2Feamena%20eamena-default-card&type=code
	- Arches forum: https://community.archesproject.org/t/card-permission/1675?u=zoometh

## Documentation

* Issue thread: [#11](https://github.com/achp-project/cultural-heritage/issues/11)
* Phil Carlisle (HE) is developping a new paradigm to handle Arches permissions at very different levels
* [ring-fencing plugin](https://github.com/eamena-project/eamena-arches-dev/tree/main/functions/permissions)