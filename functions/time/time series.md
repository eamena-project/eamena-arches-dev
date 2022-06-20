# Temporal series of Cultural Heritages damages during the Syrian conflict
> CAA 2022, communication for the [S07 session](https://github.com/eamena-oxford/eamena-arches-dev/blob/main/event/CAA-S07.md#s07-cultural-heritage-data-across-borders-web-based-management-platforms-for-immovable-cultural-heritage-in-the-global-south)

The Middle East is one of the regions with the highest concentration of cultural heritage in the world...

The dataset studied records the evaluation of conditions recording the cause of damage (e.g. a plough) and activity (e.g. agriculture) in the form of CIDOC-CRM ontologies (ISO 21127:2006) and controlled vocabularies developed by Arches/EAMENA for 19 Syrian sites.

Multi-temporal satellite imagery where "the damage visible on the imagery must have occurred before the date of acquisition of that image, and if the same damage is not visible on an image acquired at an earlier date, we assume that the damage occurred between these two dates".
The temporal dimension of the observed damage was recorded using the Extended Date/Time Format (EDTF) - an extension of the ISO 8601 standard [^0]- compliant with the Arches architecture [^1]. EDTF records allow to manage temporal uncertainty and to conduct temporal analyses (spatio-temporal, aoristic, etc.) on the dynamics of CH. The development of R scripts to routinely perform these analyses also provides an effective tool for knowledge representation and replicability of analyses.

Using iso-standards for damage assessment and temporal dynamics, the open-source database Arches and the R script, as well as our work on Linked Open Data (LOD) and FAIR science [^2].

https://github.com/zoometh/Rdev/tree/master/time

[^0]: http://www.loc.gov/standards/datetime/
[^1]: https://github.com/coherit/edtf-arches-hip#level-0-iso-8601-features
[^2]: Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., Appleton, G., Axton, M., Baak, A., … Others. (2016). The FAIR Guiding Principles for scientific data management and stewardship. Scientific data, 3(1), 1–9. doi:10.1038/sdata.2016.18

