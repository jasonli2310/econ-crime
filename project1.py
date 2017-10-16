import numpy
import csv
import json
import requests


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


def addZipcode():
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


with open('homicideWithZip.json') as data_file:
    myData = json.load(data_file)



for idx, item in enumerate(myData):
    if 'zipcode' in item:
        pass
    else:
        myData.remove(myData[idx])


homicideByZipYear = {}

for idx, case in enumerate(myData):

    if case['zipcode'] != None:

        if (case['zipcode'] in homicideByZipYear):
            if case['date'][6:10] in homicideByZipYear[case['zipcode']]:
                homicideByZipYear[case['zipcode']][case['date'][6:10]] += 1
            else:
                homicideByZipYear[case['zipcode']][case['date'][6:10]] = 1
        else:
            homicideByZipYear[case['zipcode']] = {case['date'][6:10]: 1}


with open('homicideByZipYear.json', 'w') as fp:
    json.dump(homicideByZipYear, fp)
