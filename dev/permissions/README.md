# User Permissions
> issue thread: [#11](https://github.com/achp-project/cultural-heritage/issues/11),Bulk-application of instance-level permissions, Built-in permissions, ...

## Aim

Hide HP coordinates for Guest users

## IT solution

### Built-in

Natively, Arches allows:

Arches Designer > Resource Model > Heritage Place > Permissions >   
    - [EAMENA](https://database.eamena.org/en/graph_designer/34cfe98e-c2c0-11ea-9026-02e7594ce0a0)

### Custom

Duplicate EAMENA card, change the configuration of the duplicated card permissions in a way it can be seen by people in a particular group (user [permission level](https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/users#eamena-new-groups))

* ~~solution 1~~
    - duplicate the `eamena-default-card`  
    - rename the duplicate `eamena-permission-card`  
(see https://community.archesproject.org/t/card-permission/1675?u=zoometh)

## Documentation

* Phil Carlisle (HE) is developping a new paradigm to handle Arches permissions at very different levels
* [ring-fencing plugin](https://github.com/eamena-project/eamena-arches-dev/tree/main/functions/permissions)