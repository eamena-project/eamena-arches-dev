Install RabbitMQ

```
sudo apt-get install rabbitmq-server
sudo apt-get install rabbit
```

Configure RabbitMQ (this is to mirror the EAMENA settings)

```
sudo rabbitmqctl add_vhost arches
sudo rabbitmqctl add_user arches (use 5wQf3J3JRUktFRW for password)
sudo rabbitmqctl set_permissions -p arches arches ".*" ".*" ".*"
```

Restart and check the status of RabbitMQ

```
sudo systemctl restart rabbitmq
sudo systemctl status rabbitmq
```

Celery should already be installed with Arches, but will not be running. To make Celery run on startup, create a systemd script. The Arches docs suggest using supervisor, which will have the same effect, but systemd is the default background task manager on Ubuntu and needs no further installation, so we use this instead of supervisor, as everything else (Apache, Elasticsearch, PostGreSQL) is already running within it, and it seems silly (to me) to install a different task manager just for Celery.

Create the file `/etc/systemd/system/celery.service`

```
[Unit]
Description=EAMENA Celery Broker Service
After=rabbitmq-server.service

[Service]
User=arches
Group=arches
WorkingDirectory=/opt/arches/eamena
ExecStart=/opt/arches/ENV/bin/python /opt/arches/eamena/manage.py celery start
Environment="PATH=/opt/arches/ENV/bin:$PATH"
Restart=always
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
```

Now activate it

```
sudo systemctl enable celery
sudo systemctl start celery
```

