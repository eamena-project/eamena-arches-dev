# Postgres for Arches basics

## Examples

Select all the data of a specific ressource from its UUID

```sql
SELECT * FROM tiles 
WHERE resourceinstanceid::text LIKE '06dd08e3-0edc-434c-b4bb-a29718342ad6'
```