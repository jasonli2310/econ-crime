import numpy as np
import csv
import json
import requests
import matplotlib.pyplot as plt
from scipy.stats import linregress

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


def generate_homicideByZipYear(arg):

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
                homicideByZipYear[case['zipcode']]['total'] += 1
                if case['date'][6:10] in homicideByZipYear[case['zipcode']]:
                    homicideByZipYear[case['zipcode']][case['date'][6:10]] += 1
                else:
                    homicideByZipYear[case['zipcode']][case['date'][6:10]] = 1
            else:
                homicideByZipYear[case['zipcode']] = {case['date'][6:10]: 1, 'total': 1}


    with open('homicideByZipYear.json', 'w') as fp:
        json.dump(homicideByZipYear, fp)


def cleanFreshmenReadiness():
    freshmenReadiness = {}
    with open('schoolComplete.csv', newline='') as csvfile:
        Readiness = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in Readiness:
            freshmenReadiness[row[2]] = {}
            freshmenReadiness[row[2]]['1997'] = row[5]
            freshmenReadiness[row[2]]['1998'] = row[6]
            freshmenReadiness[row[2]]['1999'] = row[7]
            freshmenReadiness[row[2]]['2000'] = row[8]
            freshmenReadiness[row[2]]['2001'] = row[9]
            freshmenReadiness[row[2]]['2002'] = row[10]
            freshmenReadiness[row[2]]['2003'] = row[11]
            freshmenReadiness[row[2]]['2004'] = row[12]
            freshmenReadiness[row[2]]['2005'] = row[13]
            freshmenReadiness[row[2]]['2006'] = row[14]
            freshmenReadiness[row[2]]['2007'] = row[15]
            freshmenReadiness[row[2]]['2008'] = row[16]
            freshmenReadiness[row[2]]['2009'] = row[17]
            freshmenReadiness[row[2]]['2010'] = row[18]
            freshmenReadiness[row[2]]['2011'] = row[19]
            freshmenReadiness[row[2]]['2012'] = row[20]
            freshmenReadiness[row[2]]['2013'] = row[21]
            freshmenReadiness[row[2]]['2014'] = row[22]
            freshmenReadiness[row[2]]['average'] = row[23]

    with open('froshReady.json', 'w') as fp:
        json.dump(freshmenReadiness, fp)


with open('homicideByZipYear.json') as data_file:
    homicideData = json.load(data_file)

with open('froshReady.json') as data_file:
    schoolData = json.load(data_file)


# print(schoolData['60621'])
# print(homicideData['60621'])


def homicidesPerYear(year):
    homicidesYear = 0

    for key in homicideData:
        if year in homicideData[key]:
            homicides2016 += homicideData[key][year]

    print(homicidesYear)

def averageHomicideByReadiness():
    pass

    xReadiness = []
    yHomicides = []

    for key in schoolData:
        if key in homicideData:
            xReadiness.append(float(schoolData[key]['average']))
            yHomicides.append(float(homicideData[key]['total']))

    print(linregress(yHomicides, xReadiness))

    # plt.scatter(xReadiness, yHomicides)
    # plt.ylabel('Total Number of Homicides 2001-2017')
    # plt.xlabel('Average Percent of Freshman Readiness 1997-2014')
    # plt.title('Homicides and Percent Freshman Readiness by Zipcode')



    fit = np.polyfit(xReadiness,yHomicides,1)
    fit_fn = np.poly1d(fit)
    # fit_fn is now a function which takes in x and returns an estimate for y

    plt.plot(xReadiness,yHomicides, 'yo', xReadiness, fit_fn(xReadiness), '--k')

    plt.ylabel('Total Number of Homicides 2001-2017')
    plt.xlabel('Average Percent of Freshman Readiness 1997-2014')
    plt.title('Homicides and Percent Freshman Readiness by Zipcode')
    plt.show()

def hom_frosh_byZip(zip):

    xReadiness = []
    yHomicides = []
    time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if (zip in homicideData) and (zip in schoolData) and (len(homicideData[zip]) == 18):

        # yHomicides.append(float(homicideData[zip]['2001']))
        # yHomicides.append(float(homicideData[zip]['2002']))
        # yHomicides.append(float(homicideData[zip]['2003']))
        # yHomicides.append(float(homicideData[zip]['2004']))
        # yHomicides.append(float(homicideData[zip]['2005']))
        yHomicides.append(float(homicideData[zip]['2006']))
        yHomicides.append(float(homicideData[zip]['2007']))
        yHomicides.append(float(homicideData[zip]['2008']))
        yHomicides.append(float(homicideData[zip]['2009']))
        yHomicides.append(float(homicideData[zip]['2010']))
        yHomicides.append(float(homicideData[zip]['2011']))
        yHomicides.append(float(homicideData[zip]['2012']))
        yHomicides.append(float(homicideData[zip]['2013']))
        yHomicides.append(float(homicideData[zip]['2014']))
        yHomicides.append(float(homicideData[zip]['2015']))
        yHomicides.append(float(homicideData[zip]['2016']))
        yHomicides.append(float(homicideData[zip]['2017']))


        xReadiness.append(float(schoolData[zip]['1997']))
        xReadiness.append(float(schoolData[zip]['1998']))
        xReadiness.append(float(schoolData[zip]['1999']))
        xReadiness.append(float(schoolData[zip]['2000']))
        xReadiness.append(float(schoolData[zip]['2001']))
        xReadiness.append(float(schoolData[zip]['2002']))
        xReadiness.append(float(schoolData[zip]['2003']))
        xReadiness.append(float(schoolData[zip]['2004']))
        xReadiness.append(float(schoolData[zip]['2005']))
        xReadiness.append(float(schoolData[zip]['2006']))
        xReadiness.append(float(schoolData[zip]['2007']))
        xReadiness.append(float(schoolData[zip]['2008']))
        # xReadiness.append(float(schoolData[zip]['2009']))
        # xReadiness.append(float(schoolData[zip]['2010']))
        # xReadiness.append(float(schoolData[zip]['2011']))
        # xReadiness.append(float(schoolData[zip]['2012']))
        # xReadiness.append(float(schoolData[zip]['2013']))

        print(linregress(xReadiness,yHomicides))

        plt.plot(time, yHomicides)
        plt.plot(time, xReadiness)
        plt.show()

# def changeInHomicide
#
# for key in schoolData:
#
#     if key in homicideData and len(homicideData[key]) == 18:
#
#         print("zipcode:  ", key)
#         print("total homicides:  ", homicideData[key]['total'])
#         print("average frosh readiness rate:  ", schoolData[key]['average'])
#         print("\n")
#         hom_frosh_byZip(key)
#         print('\n\n\n')

#hom_frosh_byZip("60609")
# print(homicideData['60630']['total'])

averageHomicideByReadiness()
