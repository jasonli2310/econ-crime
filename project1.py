import numpy
import csv
import json
import requests
from geopy.geocoders import Nominatim
geolocator = Nominatim()


def cleanData():

    myData = []

    with open('Homicide_Map.csv', newline='') as csvfile:
        homicideData = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in homicideData:
            newdict = {}
            newdict['caseNumber']  = row[0]
            newdict['date'] = row[2]
            newdict['locationType'] = row[7]
            newdict['lat'] = row[-4]
            newdict['long'] = row[-3]
            myData.append(newdict)

    with open('homicideChicago.json', 'w') as fp:
        json.dump(myData, fp)


with open('homicideChicago.json') as data_file:
    myData = json.load(data_file)




#
# testUrl = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+40.714224+","+-73.961452+"&key=AIzaSyB0hMeyy5OEw79210qxgrics9BgxB6YZxU"
# response = requests.get(testUrl)
#
# print(response.json()['results'][0]['formatted_address'])
# print(response.json(['results'][0]['formatted_address']))
# print(len(myData))
#
for event in myData[1:100]:
    xyCoordinate = event['lat'] + ',' + event['long']

    eventURL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+xyCoordinate+"&key=AIzaSyB0hMeyy5OEw79210qxgrics9BgxB6YZxU"
    response = requests.get(eventURL)

    print(response.json()['results'][0]['formatted_address'].split(" ")[-2].rstrip(','))



    # eventLocation = geolocator.reverse(xyCoordinate)[0].split(",")
    # event["location"] = eventLocation
    #
    # print(event["location"])

#
#         myData.append(row)
#
#
# for event in myData[1:5]:
#     myLat = event[-4]
#     myLong = event[-3]
#     a = myLat + ', ' + myLong
#     myLocation = geolocator.reverse(a)[0].split(",")
#     event[3] = myLocation
#
#
# print(myData[1])
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
