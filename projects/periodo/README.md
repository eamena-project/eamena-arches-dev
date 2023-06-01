# PeriodO / EAMENA
> https://perio.do/en/

The aim is to export EAMENA cultural periods and subperiods as new entries in PeriodO 

## Workflow

* EAMENA has these periods or subperiods: https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/periodo/cultural_periods.tsv
* Ryan Shaw (`@rybesh`) sent a JSON [template](https://gist.github.com/rybesh/9f64c127ad8eeb69619896f22064bb0e#file-example-dataset-json) for data entry into PeriodO
* This template has been updated with EAMENA data[^2]: https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/periodo/template_eamena.json
* TODO: this process has to automated to all EAMENA periods and subperiods[^3]

## PeriodO Example

An example of the `Predynastic` JSON is here: https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/periodo/periodo-period-cp44786m7.json [^1].

<p align="center">
  <img alt="img-name" src="../../www/periodo-json-template-predynastic.png" width="400">
  <br>
    <em>screenshot of the `Predynastic` record in PeriodO</em>
</p>





---

The PeriodO issue thread: https://github.com/eamena-project/eamena-arches-dev/issues/12

[^1]: This example corresponding to the URL: https://client.perio.do/?page=period-view&backendID=web-https%3A%2F%2Fdata.perio.do%2F&authorityID=p0cp447&periodID=p0cp44786m7
[^2]: this template has been modified for the EAMENA cultural period `Chalcolithic (Northern Iran) ` (see its temporal bounds [here](https://github.com/eamena-project/eamena-arches-dev/blob/main/projects/periodo/cultural_periods.tsv#L2))
[^3]; PeriodO's `PartOf` is in some ways equivalent to the hierarchical structure of EAMENA

