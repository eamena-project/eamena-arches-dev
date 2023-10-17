# AWS

## Instances

| name 	| type 	| vCPUs 	| memory (GiB) | storage (GiB) | storage used % 	| price (per month, $)	| notes 	| date 	|
|------	|------	|-------	|--------|--------|---------------	|-------	|-------	|------	|
| 24test - KAHD | t2.xlarge	| 4 | 16 | 18 | 74 | 147 | Arches v5.2, over-provisioned | 23-10-09
| EAMENA | m6g.4xlarge	| 16  | 64 | 350 | 19	| 502 | Arches v7.3, under-provisioned | 23-10-09

instance type: see https://instances.vantage.sh/aws/ec2/t2.xlarge or https://aws.amazon.com/ec2/instance-types/

## Pricing

### Instances
> per month, available zone = Ireland

* t2.xlarge:
	- On Demand: $147.17
	- 1 Yr Reserved: $103.51
	- 3 Yr Reserved: ...
	- Spot: ...

### Forecast

* full costings of a prepaid, 3 Yr Reserved instance for a KAHD upgrade to Arches v7 using the same specs it currently has;
* full costings of a prepaid, 3 Yr Reserved instance for a smaller Syrian instance;


---
links:
* [Arches system requirements](https://arches.readthedocs.io/en/stable/installing/requirements-and-dependencies/#system-requirements)








