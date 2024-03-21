# IIIF
> International Image Interoperability Framework, IIIF standard, triple-I-F

## Training Agenda
> by Galen Mancino

For Arches v5.2

- Cantaloupe (IIIF Server) backend setup
- Arches-IIIF related frontend setup
- Demo / Questions

## Cantaloupe (IIIF Server) Backend Setup

- Download Cantaloupe (Only the latest version of 4 has been actively tested by the Arches community. Cantaloupe 5 is considered unstable for our purposes)
- Copy the `cantaloupe.properties.sample` file into one called `cantaloupe.properties` edit it to (at a minimum) set the `FilesystemSource.BasicLookupStrategy.path_prefix` to the absolute path of the “uploadedfiles” directory inside the project subdirectory e.g. `/home/archesadmin/test_project/test_project/uploadedfiles/`
- Ensure that the setting `CANTALOUPE_DIR` in the project `settings.py` file is: `os.path.join(APP_ROOT "uploadedfiles")`
- Ensure that the Image Service Manager is visible in the navbar. To change update the “config” column for the “Image Service Manager” plugin in your database (see code snippet)
- Run the Cantaloupe server from the command line

### Cantaloupe Backend Setup Code Snippets

```bash
cd archesadmin
mkdir cantaloupe
cd cantaloupe
wget https://github.com/cantaloupe-project/cantaloupe/releases/download/v4.1.11/cantaloupe-4.1.11.zip
sudo apt install unzip
mkdir cantaloupe
unzip -j cantaloupe-4.1.11.zip -d cantaloupe
cd cantaloupe
cp cantaloupe.properties.sample cantaloupe.properties
sudo -u postgres psql -d test_project -c "update plugins set config = '{"show":true}' where name = 'Image Service Manager';"
java -Dcantaloupe.config=./cantaloupe.properties -Xmx2g -jar cantaloupe-4.1.11.war
apt install default-jre
```

## Arches-IIIF Related Frontend Setup

There are 2 parts here:

1. Create an “Image Service” and upload images to it. These will be available as “IIIF Manifests” or sometimes just called “Manifests.”
2. Create a nodegroup in a resource model to create IIIF Annotation data.

### Arches-IIIF Related Frontend Setup - 1

- Create an “Image Service” by clicking “Image Service Manager” on the vertical navbar.
- Click “Create a new Service” and upload at least 1 image.
- Click the “Canvas” tab to upload additional images at any time. All images in the set are associated with a single “Manifest.”
- Now you can create annotation data for the image(s) in your manifest.

### Arches-IIIF Related Frontend Setup - 2

- Go to a new or existing Resource Model and create a node with datatype: “semantic.”
- In the “Cards” tab (aka the Card manager) select the “IIIF Card” as the Card Type for this node.
- Go back to the “Graph” tab (aka the Graph Designer) and add a child node to this node. This child node must be datatype: “annotation.”
- Add as sibling nodes to this annotation node any other nodes that you would like to accompany the annotation e.g., dates, related resources (resource-instance datatype), text, etc. These pieces of data will be saved in the same tile as the annotation.
- Now you’re ready to create annotations.

## Demo: Creating Annotations

- Image Format: JPEG
- Dimensions: 1000 x 565
- Image Format: Portable Network Graphic (PNG)
- Bits Per Pixel: 24
- Color: Truecolor
- Dimensions: 1000 x 565
- Interlaced: Yes

(Repeated demo steps with JPEG and PNG formats are mentioned multiple times with the same details.)

---

This Markdown format provides a structured document that mirrors the content and organization of the original PDF, ready for use in Markdown-compatible platforms or documentation systems.
# Other

glitch with Arches (solved now): https://github.com/archesproject/arches/issues/8419