Arches 7.3 requires Elasticsearch 8.3.3. I have tried EAMENA v3 with this version of Elasticsearch and it doesn't appear to work, so if upgrading from EAMENA v3, this must be stopped and removed before Elasticsearch is upgraded, if installing on the same VM.

## Download and run Elasticsearch

```bash
wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-amd64.deb"
sudo dpkg -i ./elasticsearch-8.3.3-amd64.deb
```

Edit `/etc/elasticsearch/elasticsearch.yml`, set the following. This removes all security, but as the VM is firewalled, this is low risk so long as there are no open Elasticsearch ports, and makes configuring Arches much simpler.

```yaml
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl:
  enabled: false
```

Finally, start/restart ElasticSearch.

```shell
sudo systemctl restart elasticsearch
```