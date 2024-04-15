# Creating a readonly Postgres user.
This documentation outlines the steps to create a read-only PostgreSQL user named 'eamenar'. A read-only user has limited privileges and can only fetch data from the database without being able to modify or delete it.

1. Connect to PostgreSQL:
Open your terminal or command prompt and connect to your PostgreSQL instance using psql:

```bash
psql -U eamenar
```
Replace 'eamenar' with your PostgreSQL administrative username if different.

2. Create a Read-Only Role:
In PostgreSQL, roles are used to manage user permissions. We will create a new role named 'eamenar' with read-only privileges:

```sql
CREATE ROLE eamenar WITH LOGIN PASSWORD 'your_password_here';
```
Replace 'your_password_here' with the desired password for the 'eamenar' user.

3. Grant Read-Only Privileges:
Next, we will grant read-only privileges to the 'eamenar' role on specific database objects. In this example, we will grant SELECT privileges on all tables in a specific database named 'your_database_name':

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO eamenar;
```
Replace 'your_database_name' with the name of your PostgreSQL database.

4. Verify Permissions:
To ensure that the 'eamenar' role has been created and configured correctly, you can list the roles and their privileges:

```sql
\du eamenar
```
This command will display the details of the 'eamenar' role, including its login status and privileges.

5. Test the Read-Only User:
Finally, test the read-only user by connecting to the PostgreSQL database using the 'eamenar' credentials and attempting to fetch data:

```bash
psql -U eamenar -d your_database_name
```
You should now be connected to the database with read-only privileges. Try querying some data to ensure that the user can fetch information but cannot modify or delete it.