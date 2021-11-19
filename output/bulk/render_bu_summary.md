# Render BU summary
> After a BU, render a short summary for the user

After the BU process, from the SSH connection, a resume can be displayed with a python command[^1]. The result is copied/pasted in a JSON file. A S&R allows to convert the UUID into an URL[^2]


<p align="center">
  <img alt="img-name" src="img/json_summary.png" width="700">
  <br>
    <em>screenshot of the JSON with URL</em>
</p>

The URL opens the Resource Report

<p align="center">
  <img alt="img-name" src="img/json_summary_uuid.png" width="700">
  <br>
    <em>screenshot of the Resource Report</em>
</p>

The Resource name can be search in the map database

<p align="center">
  <img alt="img-name" src="img/json_summary_uuid_search.png" width="700">
  <br>
    <em>screenshot of the Resource Report</em>
</p>


[^1]: `python /opt/arches/eamena/manage.py bu -o summary -s "*filename*.json" | json_pp`
[^2]: Search: `"uuid" : "`, Replace by `"uuid" : "https://database.eamena.org/en/report/`
