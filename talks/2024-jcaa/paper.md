# EAMENA, a framework for cultural heritage and archaeological data management

## Introduction

... deployed on the top of Arches

Destruction of Palmyra in 2016 by ISIS.
The purpose was to map extansively the endangered cultural heritage in the Arabic speaking region, from Mauritania to Irak. And more recently covers Iran and Afghanistan. Identifying threats and causes of disturbances (Agricultural, Urbanist, etc.). To cover the scope of the project, and because of the difficulties to access field work (either for being in desertic remote areas and because of security issues) remote sensing has been the privilegied method to assess this cultural heritage. So far, EAMENA comprehensive surveys has led to the discovery of XXX new kites structures and 3 roman forts, among other.

## Design & Architecture

**EAMENA** platform is deployed on the top of the NoSQL **Arches** stack of open-source softwares. Arches serves as a semantic web-based purpose-built platform for inamovible cultural heritage management. 


<br>
<img src="https://raw.githubusercontent.com/eamena-project/eamena-arches-dev/main/www/arches-ea-stack.png" width="800px">
<br>


**Arches** key features are its logics based on Python, from far the world-wide most used programming language (REF Tiobe) and JavaScript object notation (JSON-LD, GeoJSON, Postgres JSONB type) the current standard to exchange data over the web. Arches lies also on mature technologies (Postgres database, Django web-application framework, Apache server among other), various iso-standards (CIDOC-CRM, Dublin Core, SKOS, SPARQL endpoint, IIIF, EDTF, WGS84/OGC) and semantic web technologies (XML, RDF, etc.). From the version 7.3, Arches supports internationalisation (i18) and is currently located (l10n) in XXX different languages. In comparison to other open-source purpose-based content management systems such as Heurist and OpenAtlas, so far, Arches  garners  more GitHub contributions and has been also significantly more forked. Moreover, ongoing developments of Arches, such as Arches for Science (also known as DISCO), can also benefit archeosciences, including IIIF, CRMSci, etc, while Arches for HERs, due to be launched later this summer with Historic England will provide a new level of access to UK data. Arches stands then as a mature and major technology for cultural heritage management.
**Arches** ~ **EAMENA** EAMENA is the oldest university-based project grounded on Arches, since 2016, in comparison to sibling projects (MAHSA and MAEASaM at the University of Cambridge; CAAL at the University of London; MAPSS at the Max Planck Institute, etc.). As so, it gathered more experiences and has a leading role in working to mke this projects interoperable for exemple by  sharing the reference data of our projects (ontologies, data models, and thesauri in XML and JSON files) through a common GitHub organization (https://github.com/achp-project).
**EAMENA** ~ **Arches** by providing the localisation in Arabic (`ar`), French (`fr`) and Central Kurdish (`cbk`).... The `citation generator` plugin was designed to help non-Western EAMENA contributors have a simple way to publish their research in Western peer-reviewed journals by following a path starting with data entry, Zenodo repository, LLM ~ data paper models, PCI recommendation and finally, publication of data paper and research paper.
**EAMENA** 

## Case Study

## Discussion

## Conclusion


## aclass

An Arches resource model is a structured data model designed for the Arches Platform. It encompasses the data structure (the entity-relationship model) and also includes the interface for entering data (forms) and generating reports for each resource model.4 The graph structure of the database allows the recording of multiple interpretations for the same resource at the field level. For example, a heritage place can have two different geometries (a point for its geometric centre and a polygon for its perimeter or a line for its path) or different archaeological interpretations with different levels of confidence made by two or more contributors.

The database incorporates controlled vocabulary. Glossaries are rooted in resources like FISH (Forum on Information Standards in Heritage) and Getty AAT (Art and Architecture Thesaurus). These vocabularies have been adapted and expanded to align with the particular needs of the EAMENA project [22]. For example, the EAMENA ‘Heritage Place Type’ could take the value ‘Archaeological Site’, which is a direct match with the AAT term ‘Archaeological site’ (aat:300000810). Other AAT and FISH terms have been adapted but are still structured data (see: https://eamena.org/advanced-use#rm-hp-fields).

**EAMENA** ~ **Arches** Bulkupload plugin