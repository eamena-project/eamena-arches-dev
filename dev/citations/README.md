> Draft for the EAMENA website

<h5 class="rtejustify" id="open-data">How to use our datasets and images</h5>

<p>Images and datasets from the EAMENA Database are under the Creative Commons Attribution 4.0 International License <a href="http://creativecommons.org/licenses/by/4.0/" rel="license"><img alt="Creative Commons Licence" src="https://i.creativecommons.org/l/by/4.0/88x31.png" style="border-width:0" style='height: 20px;vertical-align: middle;'/></a></p>

<h5 class="rtejustify" id="cite-data">How to cite an EAMENA dataset</h5>

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

<h5 class="rtejustify" id="publish-data">How to publish EAMENA data</h5>

<p>The EAMENA team is working on creating an option, called `citation-generator`, allowing the export of a dataset to Zenodo. By doing this, EAMENA contributors will obtain a citable unique reference identifier (DOI) that can be referenced in a data or research paper. Currently, this workflow has been set up in a Jupyter Notebook hosted on <a href="https://github.com/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb">GitHub</a> and <a href="https://colab.research.google.com/github/eamena-project/eamena-arches-dev/blob/main/dev/citations/citation_generator.ipynb">Google Colab</a>.</p>

<p style="text-align: center;">
<img alt="citation-generator" src="https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/arches-v7-export-citation.png" width="500" style="border-width:0" /><br>
<em>Future export mode in the EAMENA main window</em>
</p>

<p>The workflow will follow these steps:
<ol>
	<li>Create a Search URL. Only one resource type should be selected (Heritage Place, Grid Square, etc.), and this will be the exported dataset. Currently, the workflow covers the export of Heritage Places and Grid Squares.</li>
	<li>Select the 'citation' button.</li>
	<li>Fill in some of the dataset metadata:</li>
	<ul>
		<li>`TITLE` of the dataset. For example: "Sistan: part 1. Heritage Places" or "Sistan: part 1. Grid Squares".</li>
		<li>`DESCRIPTION` of the dataset. For example: "Deposit of Heritage Places from the Sistan region (Iran, Afghanistan) maintained within the EAMENA database" or "Deposit of Grid Squares from the Sistan region (Iran, Afghanistan) maintained within the EAMENA database".</li>
		<li>`FILENAME` of the dataset. For example: "sistan_part1_hps" or "sistan_part1_gs".</li>
	</ul>
</ol>
<p>The other metadata will be calculated from the data themselves.</p> 

<p>The result of this deposit in Zenodo can be seen here: <a href="https://sandbox.zenodo.org/records/5847">https://sandbox.zenodo.org/records/5847</a>.
</p>

<p style="text-align:center;">
<a href="https://zenodo.org/communities/eamena" rel="license"><img alt="citation-generator" src="https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/zenodo-communities-eamena.png" width="500" style="border-width:0" /></a><br>
<em>EAMENA datasets, GeoJSON files, will be hosted under Zenodo's `eamena` community (https://zenodo.org/communities/eamena) and referenced by DOI.</em>
</p>



