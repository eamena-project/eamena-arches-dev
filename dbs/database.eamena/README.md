# EAMENA DB

## Timeline

DB migration process

```mermaid
gantt
    title EAMENA v4 Arches v7 training
    dateFormat  YYYY-MM-DD
    axisFormat  %d-%m
    tickInterval 7day
    section EAMENA v3
    Arches v5.2              : a0, 2023-01-01, 2023-04-24
    Arches v5.2 stopped      : a0, 2023-04-28, 2023-05-09
    section EAMENA v3 -> v4
    Arches v7.3 DB installation        : a1, 2023-03-06, 2d
    Arches v7.3 Graphs installation    : a1, 2023-03-06, 2d
    Arches v7.3 Data                   : a1, 2023-04-10, 4d
    Arches v7.3 Custom components      : a1, 2023-04-10, 4d
    section EAMENA v4
    Arches v7.3 tests                  : a1, 2023-04-17, 5d
    Arches v7.3 showcase               : a1, 2023-04-25, 1d
    Arches v7.3 public realease        : a1, 2023-05-09, 2023-10-01
```

## Customization

### Landing page

To give a new "skin" to the landing page of EAv4, we can change the background images and captions of the slides. 

<p align="center">
  <img alt="img-name" src="../../www/arches-v7-landingpage.png" width="700">
  <br>
    <em>Current landing page of EAMENA v4 <https://database.eamena.org/> </em>
</p>

Change directly the file: https://github.com/eamena-project/eamena-arches-dev/blob/main/dbs/database.eamena/varia/index.htm (paths and captions). And add the images in this folder: https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/img

* example for [Slide 1](https://github.com/eamena-project/eamena-arches-dev/blob/11df37b9c528e4e3b423ae00464190432bd69c0c/dbs/database.eamena/varia/index.htm#L255-L275)

1. Change the [image](https://github.com/eamena-project/eamena-arches-dev/blob/11df37b9c528e4e3b423ae00464190432bd69c0c/dbs/database.eamena/varia/index.htm#L258) [^1]
2. Change the [caption](https://github.com/eamena-project/eamena-arches-dev/blob/11df37b9c528e4e3b423ae00464190432bd69c0c/dbs/database.eamena/varia/index.htm#L273) [^2]

[^1]: `index.htm` -> `/opt/arches/eamena/eamena/templates`
[^2]: images -> `/opt/arches/eamena/eamena/media/img/landing/eamena`
