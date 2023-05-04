# 24test
> for KRG

## Customize the landing page

<img>

<p align="center">
  <img alt="img-name" src="../../www/arches-v5-landingpage.png" width="600">
  <br>
    <em>Landing page</em>
</p>

image : https://github.com/eamena-project/eamena-arches-dev/blob/da9d4efc80119df549e8029de75b5ce47d1027df/dbs/24test/index.htm#L171
db name: https://github.com/eamena-project/eamena-arches-dev/blob/da9d4efc80119df549e8029de75b5ce47d1027df/dbs/24test/index.htm#L176
image caption: https://github.com/eamena-project/eamena-arches-dev/blob/da9d4efc80119df549e8029de75b5ce47d1027df/dbs/24test/index.htm#L184

## Import missing Resource Models

* IR
```python manage.py packages -o import_graphs -s './packages/220607_pkg/graphs/resource_models/Information Resource.json'```

* GS
```python manage.py packages -o import_graphs -s './packages/220607_pkg/graphs/resource_models/Grid Square.json'```

* PS
```python manage.py packages -o import_graphs -s './packages/220607_pkg/graphs/resource_models/Person-Organization.json'```

* DCA
```python manage.py packages -o import_graphs -s './packages/220607_pkg/graphs/resource_models/Detailed Condition Assessment.json'```
