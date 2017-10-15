import numpy
import csv
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.reverse("52.509669, 13.376294")

myData = []

with open('Homicide_Map.csv', newline='') as csvfile:
    homicideData = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in homicideData:
        myData.append(row)


for event in myData[1:5]:
    myLat = event[-4]
    myLong = event[-3]
    a = myLat + ', ' + myLong
    myLocation = geolocator.reverse(a)[0].split(",")
    event[3] = myLocation


print(myData[1])
#
# print(myData[1][3])
#
# myLat = myData[1][-4]
# myLong = myData[1][-3]
#
# a = myLat + ', ' + myLong
#
# print(a)
#
# myLocation = geolocator.reverse(a)[0]
#
# addressArray = myLocation.split(",")
#
# print(addressArray)
