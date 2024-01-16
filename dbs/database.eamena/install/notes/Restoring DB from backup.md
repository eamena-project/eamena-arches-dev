### Restoring the Database

Sometimes, the database will need to be restored from its latest backup. This is the process for doing that. Everything needs to be done via a command line shell on the AWS machine.

As `ubuntu`user, stop Apache gracefully (ie allow existing connections to terminate)...
```
sudo apache2ctl graceful-stop
```

As `arches` user, find and extract the latest `arches-prod-backup-` file...
```
cd /opt/arches/nightly_backups/
ls -l | grep prod-backup
```

The file will be called `arches-prod-backup-YYYY-MM-DD.tgz`.
```
tar xvzf arches-prod-backup-YYYY-MM-DD.tgz eamenadb.sql # use real filename
```

Still as `arches` user, access PostGreSQL...
```
psql -U postgres
DROP DATABASE eamena
```
if this works, all well and good. If it doesn't, and PostGreSQL complains that there is a connection to the database, repeat the previous command but with `WITH (FORCE)` on the end...
```
DROP DATABASE eamena WITH (FORCE)
```
Now get out of PostGreSQL using Ctrl+D. The database is now empty.

Now we import the backup file into the database from the Linux command line...
```
psql -U postgres < eamenadb.sql
```
This will take a while and the screen will fill with output. The command should finish by dropping you back to the command line. The database has now been restored.

Now, as the `ubuntu` user...
```
sudo systemctl status apache2
```
will restart Apache.  You should now be able to access the database from  web browser, but the search will not work until you run a reindex.

### Running a Re-Index
There is a BASH shell script in the Arches home directory for doing this. It takes about 10 hours to run, during which time the search will not be available, so this should only be done at night or at the weekend. It doesn't require any interaction, so feel free to run the script, log off and go to bed.

As the `arches` user...
```
cd /opt/arches/scripts
nohup ./reindex.sh &
```

Note the '&' on the end of the second line. This makes the script run in the background, returning you to the command line. If you forget this, no problem, simply press Ctrl+Z to suspend the script, then type...
```
bg
```
to force the suspended script into the background. To check the script is indeed running, type....
```
ps x
```
...to get a process list, and look for a line containing the following...
```
/opt/arches/ENV/bin/python /opt/arches/eamena/manage.py es index_database
```
...or very similar.

Once the reindex is running, press Ctrl+D to exit the shell and all should be well once it finishes.
