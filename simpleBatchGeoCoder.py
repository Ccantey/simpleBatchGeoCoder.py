import csv
from geopy.geocoders import GoogleV3
geolocator = GoogleV3('AIzaSyCU7Dy7nV2cJ5md6qSnSTeNvFCSbLQkEP0')

###BasicAPI
##location = geolocator.geocode('10351 Ash River Trail Orr MN')
##print location.latitude

# some csv file with a minimum of an address field, city field, zip code field
with open('C:\\Users\\ccantey\\Desktop\\BatchGeoCode - 01-20-2016\\inputs\\LegacyReport 01-06-2016.csv', 'rb')as csvinput:
    # output file/location
    with open('C:\\Users\\ccantey\\Desktop\\output.csv', 'w') as csvoutput:
        reader = csv.DictReader(csvinput, delimiter=',')
        
        latlong = ['field_lat_long']
        writer = csv.DictWriter(csvoutput, fieldnames=latlong, lineterminator='\n')
        writer.writeheader()  
  
        for row in reader:

            #print row['Address'], row['City '], row['zip code']
            fullAddress = row["field_address"] + ', ' + row["field_city"] +',MN ' + row["field_zip"]

            location = geolocator.geocode(fullAddress)
            
            if len(row["field_city"]) < 2:
                geocodelatitude = 'none'
                geocodelongitude = 'none'
                writer.writerow({'field_lat_long': geocodelatitude})
            else:
                try:
                    geocodelatitude = location.latitude
                    geocodelongitude =location.longitude
                    LatLong = str(geocodelatitude) + '|' + str(geocodelongitude)
                    writer.writerow({'field_lat_long': LatLong})
                    
                except:
                    geocodelatitude = 'No Match'
                    geocodelongitude = 'No Match'
                    LatLong = 'No Match'
                    writer.writerow({'field_lat_long': geocodelatitude})


            print "ID",row['field_custom_id'],", field_lat_long: ", str(geocodelatitude) + '|' + str(geocodelongitude)


