# Creating a read-only user 
> *by* Reuben Osborne

1. Connect to your PostgreSQL database as a superuser or a user with appropriate privileges. `
```
psql -U postgres
```

2. Create the read-only user using the `CREATE USER` command. Replace `<username>` with the desired username and `<password>` with the user's password:

```sql
CREATE USER <username> WITH PASSWORD '<password>';
```

3. Grant read-only privileges to the user on the desired database. You can do this by using the `GRANT` command. For example, to grant read-only access to a database named `<database_name>`:

```sql
GRANT CONNECT ON DATABASE <database_name> TO <username>;
```

4. Grant SELECT privileges on the specific tables or schemas to restrict access to read-only. For example, to grant read-only access to all tables in a schema named `<schema_name>`:

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA <schema_name> TO <username>;
```

Or, if you want to grant read-only access to a specific table:

```sql
GRANT SELECT ON <table_name> TO <username>;
```

5. Finally, you should revoke any unnecessary privileges to ensure that the user remains read-only. For example, you might want to revoke the ability to create tables:

```sql
REVOKE CREATE ON SCHEMA public FROM <username>;
```

## Notes
- The main database should be called `eamena`.
- You can access this using the default `postgres` user.
- The `eamena` database is in the `public` schema.
- Depending on your requirements you might want to only grant acccess to specific tables. E.g `tiles`. 
