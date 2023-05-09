EAMENA v4 Release Notes
=======================

9th May, 2023

Known Problems
--------------

* BULK UPLOADER - Currently this does not open. Although the URL endpoints are
  in the urls.py file, they are not being registered. I currently have no idea
  why this is happening, but I anticipate that it is some kind of config
  issue; the full functionality works just fine on my Arches 7 test install.

* EAMENA FORM CARD - Currently, creating a new Heritage Place and clicking on
  the geometries section causes the HTML to become unreadable. This seems to
  happen if one opens an instance of the map card (eg the geometries node)
  after opening an instance of the EAMENA form card (eg any other first-level
  node) so I believe this is just the two cards not playing well with each
  other. I believe I can fix this, but will contact Farallon if I have
  difficulty.

* PERMISSIONS <a name="permis"></a>- Users and groups between EAMENA 3 and EAMENA 4 have the same
  IDs so they map one-to-one. Sadly, due to the increased number of possible 
  permissions in Arches 7, the actual permissions do not have a direct
  mapping any more, so I will need to write a script to apply all the
  previously assigned permissions to the new user database. This script will
  modify the Django database directly via SQL. I know exactly how this
  will happen, I simply did not have time before the DB went live, and
  this currently only affects people with custom permissions, which is a
  small minority.

