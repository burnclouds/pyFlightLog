from logpy import *
from greatcircle import printTrips
from datetime import date, timedelta
from math import log10
import sys, argparse, csv

def processAirports(data):
    airports = dict() # create an empty dictionary
    for row in data:
        try:
            row[0]
        except:
            continue
        portID = row[0].upper()
        airports[portID]=Airport(row)
    return airports

def processPlanes(data):
    planes = dict() # create an empty dictionary
    models = dict() # create an empty dictionary
    types = dict() # create an empty dictionary
    for row in data:
        try:
            row[0]
        except:
            continue
        Nnum = row[0].upper()
        Model = row[1].upper()
        Type = row[2].upper()
        rg = row[3]
        hp = row[4]
        tw = row[5]
        planes[Nnum] = Planes(Model,Type)

        if Model in models:
            models[Model].addPlane()
        else:
            models[Model] = Models(Type,rg,hp,tw)

        if Type in types:
            types[Type].addPlane()
        else:
            types[Type] = Types()

    return planes, models, types

def processStudents(data):
    students = dict() # create an empty dictionary
    for row in data:
        try:
            row[0]
        except:
            continue
        studentROM = int(log10(len(data))+1) # Student ID leading zeros
        sID = row[0].zfill(studentROM)
        last = row[1]
        first = row[2]
        students[sID] = Student(last,first)
    return students, studentROM

def processLogbook(data, stdntROM, airports, planes, models, types, students, trips):
    book = list() # create an empty list
    for row in data:
        try:
            #skip header/footer lines and lines with no year
            if row[0]=='' or row[0].upper()=='YEAR': continue
        except:
            continue
        l=Log(row,stdntROM)
        book.append(l)

        # if the great circle distance between these two airports is >= 50nm
        # the number of cross-country hours is equal to the hours of the flight
        dist =  airports[l.DepInd].dist(airports[l.DesInd])
#Airports
        if dist>=50:
            xc = l.Hours
            airports[l.DepInd].addXc(l.Date,l.Hours)
            airports[l.DesInd].addXc(l.Date,l.Hours)
        else:
            xc = 0
            airports[l.DepInd].addLocal(l.Date,l.Hours)
            if (l.DepInd != l.DesInd):
                airports[l.DesInd].addLocal(l.Date,l.Hours)

# Planes, Models, Types        
        planes[l.PlaneInd].addLogEntry(l.Date,l.Hours,l.Night,l.Ifr,l.Gad,xc,l.Cfi,l.Dual,l.Pic,l.Sic,l.Sft)
        models[planes[l.PlaneInd].Model].addLogEntry(l.Date,l.Hours,l.Night,l.Ifr,l.Gad,xc,l.Cfi,l.Dual,l.Pic,l.Sic,l.Sft)
        types[planes[l.PlaneInd].Type].addLogEntry(l.Date,l.Hours)

# Students
        if l.StudentInd != '':
            students[l.StudentInd].addStudentHours(l.Date,l.Cfi)

# Trips
        if l.DepInd != l.DesInd:
            # fwd/rev here is reelative to current flight not already defined trip(s)
            fwd = l.DepInd+':'+l.DesInd
            rev = l.DesInd+':'+l.DepInd
            if fwd not in trips.keys():
                if rev not in trips.keys():
                    # create new trip
                    trips[fwd] = Trips(l.Date,l.Hours,dist)
                else:
                    # reverse trip exists, add revTime
                    trips[rev].addRevTrip(l.Date,l.Hours)
            else:
                # forward trip exists, add time
                trips[fwd].addTrip(l.Date,l.Hours)

def main():
    parser = argparse.ArgumentParser(description='Logbook processer')
    parser.add_argument("-a","-A", action="store_true", help="Option to prompt for filter options")
    args = parser.parse_args()
    del parser

    inputFilePath='./'
    #inputFilePrefix='input_'
    #inputFileExtension='.txt'
    #files=('airports','planes','students')
    fqFiles = {}
    #for fname in files:
    #    fqFiles[fname] = inputFilePath+inputFilePrefix+fname+inputFileExtension
    fqFiles = {'logbook': inputFilePath+'logbook.csv',
               'airports': inputFilePath+'input_airports.txt',
               'planes': inputFilePath+'input_planes.txt',
               'students': inputFilePath+'input_students.txt'}

    stored={}
    for key, fname in fqFiles.items():
        stored[key]=[]
        with open(fname, 'r') as csvfile:
            reader=csv.reader(csvfile, delimiter=',')
            for row in reader:
                stored[key].append(row)
    del fqFiles

    airports = processAirports(stored['airports'])
    planes, models, types = processPlanes(stored['planes'])
    students, studentROM = processStudents(stored['students'])
    trips = dict() # create an empty dictionary
    processLogbook(stored['logbook'], studentROM, airports, planes, models, types, students, trips) 


    # print Trips sorted/filtered by Miles>=50 and To or From MWO
    printTrips(trips, airports, 'Miles', 50, 'MWO')
    # print all trips sorted by Flights (no filters)
    printTrips(trips, airports, 'Flights', None, None)






main()
