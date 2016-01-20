# BatchGeoCode

=====================================

This Python program depends on a geopy python wrapper and a Google API key. It will read a csv file with an address field that can contain many addresses, delimited by a '|'. It depends on a master pre-geocoded library (csv). It will determine if an address already exists in the library, if not, it will geocode the address. Through the Google geocoding API, you can geocode up to 2,500 address per day. The Geopy wrapper has methods for serveral geocoding services though, so one could try/except through many more addresses.

When run, the program will open a Tkinter dialog box. The user can File-> Run: select file to be gecoded, select library key. The output will be another csv with a matching id field and the resultant geocoded (lat/lng) addresses delimited by with a "^".


First install GeoPy using [pip](http://www.pip-installer.org/en/latest/) with:

    pip install geopy

[GeoPy API](https://github.com/geopy/geopy)
