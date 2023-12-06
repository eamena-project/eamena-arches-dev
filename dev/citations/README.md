> Draft for the EAMENA website

<h5 class="rtejustify" id="open-data">How to use our datasets and images</h5>

<p>Images and datasets from the EAMENA Database can be used according to our licence: Creative Commons Attribution 4.0 International License<a href="http://creativecommons.org/licenses/by/4.0/" rel="license"><img alt="Creative Commons Licence" src="https://i.creativecommons.org/l/by/4.0/88x31.png" style="border-width:0" style='height: 50px;vertical-align: middle;'/></a></p>

<h5 class="rtejustify" id="cite-data">How to cite an EAMENA dataset</h5>
<p>
	<br />
	<span href="http://purl.org/dc/dcmitype/Dataset" property="dct:title" rel="dct:type" xmlns:dct="http://purl.org/dc/terms/">EAMENA Database</span> by <a href="https://eamena.org" property="cc:attributionName" rel="cc:attributionURL" xmlns:cc="http://creativecommons.org/ns#">EAMENA</a>        is licensed under a <a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Creative Commons Attribution 4.0 International License</a>.
	<br /> Based on a work at <a href="https://database.eamena.org">https://database.eamena.org</a></p>

<p>To cite our database please use the following (examples):</p>

<h6 class="rtejustify" id="cite-data-APA">APA</h6>
EAMENA database. (2023). Sistan: part 1. Heritage Places [Data set]. Zenodo. https://doi.org/10.5072/zenodo.5847
<h6 class="rtejustify" id="cite-data-Harvard">Harvard</h6>
EAMENA database (2023) “Sistan: part 1. Heritage Places”. Zenodo. doi: 10.5072/zenodo.5847.
<h6 class="rtejustify" id="open-data-BibTex">BibTex</h6>
<pre><code data-trim id="awesomecpp">
@dataset{eamena_database_2023_5847,
  author       = {EAMENA database},
  title        = {Sistan: part 1. Heritage Places},
  month        = dec,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5072/zenodo.5847},
  url          = {https://doi.org/10.5072/zenodo.5847}
}
</code></pre>
<h4 class="rtejustify">Updates and more information</h4>

<p class="rtejustify">As with all databases, this resource is a work in progress and is constantly being developed. Please do keep visiting the website and database for changes, as we will be adding new sites, case studies and features throughout 2023 and beyond. We will announce updates via our Twitter account. Unfortunately, it is not possible to make every record fully accessible because our main focus has to be on ensuring the protection and preservation of archaeological sites.&nbsp;Our Open Access policy
and levels of access can be&nbsp;found&nbsp;<a href="https://eamena.web.ox.ac.uk/article/eamena-marea-open-access-policy">here</a>.</p>

<h5 class="rtejustify" id="publish-data">How to publish EAMENA data</h5>

<p>The EAMENA team is working on creating an option, called `citation-generator`, allowing the export of a dataset to Zenodo. By doing this, EAMENA contributors will obtain a citable unique reference identifier (DOI) that can be referenced in a data or research paper. Currently, this workflow has been set up in a Jupyter Notebook hosted on <a href="https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb">GitHub</a> and <a href="https://colab.research.google.com/github/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb">Google Colab</a>.</p>

<p style="text-align: center;">
<img alt="citation-generator" src="https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/arches-v7-export-citation.png" width="500" style="border-width:0" /><br>
<em>Future export mode in the EAMENA main window</em>
</p>

<p>The workflow will follow these steps:
<ul>
	<li>Create a Search URL. Only one resource type should be selected (Heritage Place, Grid Square, etc.), and this will be the exported dataset. Currently, the workflow covers the export of Heritage Places and Grid Squares.</li>
	<li>Select the 'citation' button.</li>
	<li>Fill in some of the dataset metadata:</li>
	<ul>
		<li>`TITLE` of the dataset. For example: "Sistan: part 1. Heritage Places" or "Sistan: part 1. Grid Squares".</li>
		<li>`DESCRIPTION` of the dataset. For example: "Deposit of Heritage Places from the Sistan region (Iran, Afghanistan) maintained within the EAMENA database" or "Deposit of Grid Squares from the Sistan region (Iran, Afghanistan) maintained within the EAMENA database".</li>
		<li>`FILENAME` of the dataset. For example: "sistan_part1_hps" or "sistan_part1_gs".</li>
	</ul>
</ul>
The other metadata will be calculated from the data themselves. The result of this deposit in Zenodo can be seen here: <a href="https://sandbox.zenodo.org/records/5847">https://sandbox.zenodo.org/records/5847</a>.
</p>

<p style="text-align: center;">
<img alt="citation-generator" src="https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/zenodo-communities-eamena.png" width="500" style="border-width:0" /><br>
<em>EAMENA dataset, GeoJSON files, will be hosted under Zenodo's `eamena` community and referenced by DOI.</em>
</p>



