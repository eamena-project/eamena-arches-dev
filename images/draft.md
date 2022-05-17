
# Describe the bug

## Blinking image

Two images appear in the Iformation Resource (IR) Report: the header image and the thumbnail (below). The header image doesn't display well and is replaced by a 'PHOTO NOT AVAILABLE' picture 

* example:
  - IR = bf28db92-47fc-41aa-86d3-5b10f2479ae9 
  - https://database.eamena.org/en/report/bf28db92-47fc-41aa-86d3-5b10f2479ae9 

## Uploading

When uploading an image to an IR, this images goes to `https://eamena-media.s3.eu-west-2.amazonaws.com/uploadedfiles/` but the image path in the Report is `APP_ROOT/files/name_of_the_image`

* example:
  - 062e337f-60ec-4240-9ccc-93874baa2c2b
  - https://database.eamena.org/en/report/062e337f-60ec-4240-9ccc-93874baa2c2b
  - https://eamena-media.s3.eu-west-2.amazonaws.com/uploadedfiles/test_img.jpg

# Pg

c712066a-8094-11ea-a6a6-02e7594ce0a0

## Query

List all the images having images coming from Flickr (= APAAME) staticflickr

```
select resourceinstanceid, tiledata from tiles 
where tiledata -> 'c712066a-8094-11ea-a6a6-02e7594ce0a0' -> 0 ->> 'url' ilike '%staticflick%'
limit 10
```

## Examples

### image link is OK

IR = 07b8ecdd-21d3-44d4-b1f1-0f0271e29310
https://database.eamena.org/en/report/07b8ecdd-21d3-44d4-b1f1-0f0271e29310

**SQL**
```
select tiledata from tiles 
where resourceinstanceid = '07b8ecdd-21d3-44d4-b1f1-0f0271e29310' 
and tiledata::jsonb ?| array['c712066a-8094-11ea-a6a6-02e7594ce0a0']
```
**Data Output**
```
{
  "c712066a-8094-11ea-a6a6-02e7594ce0a0": [
    {
      "url": "https://eamena-media.s3.eu-west-2.amazonaws.com/uploadedfiles/4907651170_11c6ef62d9_c.jpg",
      "name": "4907651170_11c6ef62d9_c.jpg",
      "size": 170642,
      "type": "image/jpeg",
      "index": 0,
      "width": 799,
      "height": 532,
      "status": "uploaded",
      "content": "blob:https://database.eamena.org/a13a24a2-ebc0-4240-bef1-af5b444ebc1c",
      "file_id": "8ebd4d66-d041-11ec-b91a-8f6b8e1db175",
      "accepted": true,
      "lastModified": 1652168906373
    }
  ]
}
```
### image link is broken

IR = 062e337f-60ec-4240-9ccc-93874baa2c2b
https://database.eamena.org/en/report/062e337f-60ec-4240-9ccc-93874baa2c2b

**SQL**
```
select tiledata from tiles 
where resourceinstanceid = '062e337f-60ec-4240-9ccc-93874baa2c2b' 
and tiledata::jsonb ?| array['c712066a-8094-11ea-a6a6-02e7594ce0a0']
```
**Data Output**
```
{
  "c712066a-8094-11ea-a6a6-02e7594ce0a0": [
    {
      "url": "/files/b43a7f50-d532-11ec-b91a-8f6b8e1db175",
      "name": "test_img.jpg",
      "size": 591533,
      "type": "image/jpeg",
      "index": 0,
      "width": 1206,
      "height": 1800,
      "status": "uploaded",
      "content": "blob:https://database.eamena.org/f3ca1fde-86ee-42da-b2a4-50f511c5cca6",
      "file_id": "b43a7f50-d532-11ec-b91a-8f6b8e1db175",
      "accepted": true,
      "lastModified": 1652698058578
    }
  ]
}
```