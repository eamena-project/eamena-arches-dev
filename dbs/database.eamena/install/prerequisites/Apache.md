```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```

Create /etc/apache2/sites-available/database.eamena.org.conf

```
sudo a2ensite database.eamena.org
sudo a2dissite 000-default.conf
sudo a2enmod rewrite
sudo apache2ctl configtest
sudo systemctl restart apache2
```

Possibly need to give executable access to `/opt/arches`...

```
cd /opt
sudo chmod 755 -R arches
```

