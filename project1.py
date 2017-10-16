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
for idx, event in enumerate(myData[1:]):
    xyCoordinate = event['lat'] + ',' + event['long']

    eventURL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+xyCoordinate+"&key=AIzaSyCANamh_uRY6Ung4FunNjg1IdPSR4m_KHg"
    response = requests.get(eventURL)

    a = response.json()['results']
    if len(a) > 0:
        myData[idx]["zipcode"] = response.json()['results'][0]['formatted_address'].split(" ")[-2].rstrip(',')
    else:
        myData[idx]["zipcode"] = None

    print(idx)

with open('homicideWithZip.json', 'w') as fp:
    json.dump(myData, fp)


# something wrong with myData[120]
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
