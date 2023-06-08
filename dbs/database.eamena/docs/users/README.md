# Users

## Permissions

### native groups

* Application Administrator
* Crowdsource Editor
* Graph Editor
* Guest
* Mobile Project Administrator
* RDM Administrator
* Resource Deleter
	```-models | resource | Can add resource
	-models | resource | Can change resource
	-models | resource | Can delete resource
	-models | resource | Can view resource
	-models | resource instance | Create resource
	-models | resource instance | Update resource
	-models | resource instance | Delete resource
	-models | resource instance | Read resource```
* Resource Editor
	```-models | card | Can add tile
	-models | card | Can change tile
	-models | card | Can view tile
	-models | card component | Can add card component
	-models | card component | Can change card component
	-models | card component | Can view card component
	-models | card x node x widget | Can add card x node x widget
	-models | card x node x widget | Can change card x node x widget
	-models | card x node x widget | Can view card x node x widget
	-models | plugin | Can view plugin
	-models | resource | Can add resource
	-models | resource | Can change resource
	-models | resource | Can view resource
	-models | resource instance | Create resource
	-models | resource instance | Update resource
	-models | resource instance | Read resource```
* Resource Reviewer
	```-models | node group | Delete
	-models | node group | Create/Update```
* System Administrator

### EAMENA former groups

native groups +

* Academic Research Condition Assessment Users
* Academic Research Users

### EAMENA new groups

| permission level | EA group name | native groups combination  | description  |
|---|---|---|---|
| 1 | Guest | Guest | same as Arches 'Guest' but cannot see: condition assessment, coordinates[^1] |
| 2 | Researcher | same as Arches 'Guest' | no edit, no add  |
| 3 | Contributor | Resource Editor + Resource Reviewer  |  can create/edit but can't delete |
| 4 | Staff | Resource Editor + Resource Reviewer + RDM Adinistrator + user management[^2] [^3] | cannot change Resource Models and System settings |
| 5 | Sys Admin | * | = superuser |

#### TODO:

* Guest: *add* no zoom

[^1]: node level
[^2]: individual permission level
[^3]: see Bijan R. user profile
