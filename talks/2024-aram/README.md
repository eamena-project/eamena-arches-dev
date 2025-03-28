# ARAM SOCIETY FOR SYRO-MESOPOTAMIAN STUDIES - conference
> https://www.aramsociety.org/conferences/current-conferences/

## Dataset
> Caravanserais and Qanats in the Khorasan region of Iran, including four provinces (North Khorasan, Razavi Khorasan, South Khorasan, and Semnan)

EAMENA Search URL

```
https://database.eamena.org/search?paging-filter=1&tiles=true&format=tilecsv&reportlink=false&precision=6&total=809&advanced-search=%5B%7B%22op%22%3A%22and%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Khorasan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea58-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22da355018-8d3b-4ab2-97a9-ae025f5ebaf2%22%7D%2C%2234cfea44-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22or%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Semnan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea58-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22da355018-8d3b-4ab2-97a9-ae025f5ebaf2%22%7D%2C%2234cfea44-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22or%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Khorasan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea58-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22bd683b8e-f0af-499f-95ea-5615bf236333%22%7D%2C%2234cfea44-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22or%22%2C%2234cfea78-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22~%22%2C%22lang%22%3A%22en%22%2C%22val%22%3A%22Semnan%22%7D%2C%2234cfea87-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%2C%7B%22op%22%3A%22and%22%2C%2234cfea58-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22bd683b8e-f0af-499f-95ea-5615bf236333%22%7D%2C%2234cfea44-c2c0-11ea-9026-02e7594ce0a0%22%3A%7B%22op%22%3A%22%22%2C%22val%22%3A%22%22%7D%7D%5D&resource-type-filter=%5B%7B%22graphid%22%3A%2234cfe98e-c2c0-11ea-9026-02e7594ce0a0%22%2C%22name%22%3A%22Heritage%20Place%22%2C%22inverted%22%3Afalse%7D%5D
```

### Site Feature Interpretation Type (EAMENA field)

* All Caravanserais have the value `Caravanserai/Khan`.
	- Site Feature Interpretation Certainty may vary for some of the caravanserais.
* All Qanats have the value `Qanat/Foggara`.


## Process

### CVNS Paths

R script [_run_2024-aram.R](https://github.com/eamena-project/eamena-arches-dev/blob/main/talks/2024-aram/_run_2024-aram.R)

#### Map

```R
d$caravanserail_paths_map
```

![alt text](image.png)

#### Profiles

```R
d$caravanserail_paths_profile
```

![alt text](image-1.png)

#### TODO

Link CVNS one with another by doing:

- Look at the map and identify HP related one with another, for example, `78` and `2` (in this direction, = directed graph) 

![alt text](image-2.png)

- Find equivalences btw ID and EAMENA ID. , running `d$ids`

| from                      | to                         |
|---------------------------|----------------------------|
| ![alt text](image-3.png)  | ![alt text](image-4.png)   |


- Fill the [caravanserail_paths_1.csv](https://github.com/eamena-project/eamena-arches-dev/blob/main/talks/2024-aram/caravanserail_paths_1.csv) file with the corresponding EAMENA ID (here: `EAMENA-0182058,EAMENA-0231535` ), adding the correct 'route' (blue = route 3 on the map)









