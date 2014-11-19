from datetime import date
class Log(object):
    Date = None
    PlaneInd = None
    DepInd = None
    DesInd = None
    DayLand = 0
    NitLand = 0
    Appr = 0
    Hours = 0
    Night = 0
    Ifr = 0
    Gad = 0
    Cfi = 0
    StudentInd = ''
    Dual = 0
    Pic = 0
    Sic = 0
    Sft = 0
    Notes = ''
    Passengers = ''

    def __init__(self,row,stdntROM):
        # data in form of:
        #YEAR,DATE,PLANE,DEP,DES,DYLAND,NILAND,APPR,HOURS,NIGHT,IFR,GAD,CFI,STDNT,DUAL,PIC,SIC,SFTY,NOTES, PASSENGERS
        # the date field is form of dDMM where the leading zero on month is required but not for the day
        year = int(row[0])
        day = int(row[1][-2:])
        month = int(row[1][:-2])
        self.Date = date(year, month, day) # date object
        self.PlaneInd = row[2].upper()
        self.DepInd = row[3].upper()
        self.DesInd = row[4].upper()
        self.DayLand = int(row[5])
        self.NitLand = int(row[6])
        self.Appr = int(row[7])
        self.Hours = int(row[8])/10.0
        self.Night = int(row[9])/10.0
        self.Ifr = int(row[10])/10.0
        self.Gad = int(row[11])/10.0
        self.Cfi = int(row[12])/10.0
        if row[13] == '0':
            self.StudentInd = ''
        else:
            self.StudentInd = row[13].zfill(stdntROM) # add leading zero to student ID
        self.Dual = int(row[14])/10.0
        self.Pic = int(row[15])/10.0
        self.Sic = int(row[16])/10.0
        self.Sft = int(row[17])/10.0
        if len(row)>19:
                self.Notes = row[18]
        if len(row)>20:
                self.Passengers = row[19]

    def getDate(self):
        return self.Date

class Airport(object):
    Title = ""
    State =""
    Lat = 0
    Lon = 0
    LocalFlights = 0
    LocalHours = 0
    XcFlights = 0
    XcHours = 0
    FirstDate = None
    LastDate = None
    LocalFirstDate = None
    LocalLastDate = None

    def __init__(self,row):
        self.Title=row[1]
        self.State=row[2]
        self.Lat=int(row[3]) + int(row[4])/60.0
        self.Lon=int(row[5]) + int(row[6])/60.0

    def addLocal(self, Date, Hours):
        if (self.LocalFirstDate == None or self.LocalFirstDate > Date):
            self.LocalFirstDate = Date
        if (self.LocalLastDate == None or self.LocalLastDate < Date):
            self.LocalLastDate = Date
        if (self.FirstDate == None or self.FirstDate > Date):
            self.FirstDate = Date
        if (self.LastDate == None or self.LastDate < Date):
            self.LastDate = Date
        self.LocalHours += Hours
        self.LocalFlights += 1

    def addXc(self, Date, Hours):
        if (self.FirstDate == None or self.FirstDate > Date):
            self.FirstDate = Date
        if (self.LastDate == None or self.LastDate < Date):
            self.LastDate = Date
        self.XcHours += Hours
        self.XcFlights += 1

    def __repr__(self):
        pass

class Types(object):
    FirstDate = None
    LastDate = None
    Flights = 0
    Hours = 0
    NumPlanes = 0

    def __init__(self):
        self.addPlane()

    def __repr__(self):
        pass

    def addPlane(self):
        self.NumPlanes += 1

    def addLogEntry(self,Date,Hours):
        if (self.FirstDate == None or self.FirstDate > Date):
            self.FirstDate = Date
        if (self.LastDate == None or self.LastDate < Date):
            self.LastDate = Date
        self.Hours += Hours
        self.Flights += 1

class Models(object):
    Type = None
    Rg = False
    Hp = False
    Tw = False
    NumPlanes = -1 # -mc why is this negative?
    FirstDate = None
    LastDate = None
    Flights = 0
    Hours = 0
    Night = 0
    Ifr = 0
    Gad = 0
    Xc = 0
    Cfi = 0
    Dual = 0
    Pic = 0
    Sic = 0
    Sft = 0

    def __init__(self,Type,Rg,Hp,Tw):
        self.Tw = True if Tw.upper() == 'TW' else False
        self.Hp = True if Hp.upper() == 'HP' else False
        self.Rg = True if Rg.upper() == 'RG' else False
        self.Type = Type.upper()
        self.addPlane()

    def __repr__(self):
        pass

    def addPlane(self):
        self.NumPlanes += 1

    def addLogEntry(self,Date,Hours,Night,Ifr,Gad,Xc,Cfi,Dual,Pic,Sic,Sft):
        if (self.FirstDate == None or self.FirstDate < Date):
            self.FirstDate = Date
        if (self.LastDate == None or self.LastDate > Date):
            self.LastDate = Date
#        if (self.NumPlanes != 10000): # -mc What is all this for?
#            if (self.NumPlanes == -1):
#                self.NumPlanes = PlaneIndex
#            if (self.NumPlanes != PlanesIndex):
#                self.NumPlanes - 10000
        self.Flights += 1
        self.Hours += Hours
        self.Night += Night
        self.Ifr += Ifr
        self.Gad += Gad
        self.Xc += Xc
        self.Cfi += Cfi
        self.Dual += Dual
        self.Pic += Pic
        self.Sic += Sic
        self.Sft += Sft

class Planes(object):
    Model = None
    Type = None
    FirstDate = None
    LastDate = None
    Flights = 0
    Hours = 0
    Night = 0
    Ifr = 0
    Gad = 0
    Xc = 0
    Cfi = 0
    Dual = 0
    Pic = 0
    Sic = 0
    Sft = 0

    def __init__(self,Model, Type):
        self.Model = Model.upper()
        self.Type = Type.upper()

    def addLogEntry(self,Date,Hours,Night,Ifr,Gad,Xc,Cfi,Dual,Pic,Sic,Sft):
        if (self.FirstDate == None or self.FirstDate > Date):
            self.FirstDate = Date
        if (self.LastDate == None or self.LastDate < Date):
            self.LastDate = Date
        self.Flights += 1
        self.Hours += Hours
        self.Night += Night
        self.Ifr += Ifr
        self.Gad += Gad
        self.Xc += Xc
        self.Cfi += Cfi
        self.Dual += Dual
        self.Pic += Pic
        self.Sic += Sic
        self.Sft += Sft

class Student(object):
    LastName = ""
    FirstName = ""
    Flights = 0
    Hours = 0
    FirstDate = None
    LastDate = None

    def __init__(self,LastName,FirstName):
        self.LastName = LastName
        self.FirstName = FirstName

    def __repr__(self):
        return self.LastName+","+self.FirstName+","+str(self.Hours)+","+str(self.Flights)

    def addStudentHours(self,Date,Hours):
        if (self.FirstDate == None or self.FirstDate > Date):
            self.FirstDate = Date
        if (self.LastDate == None or self.LastDate < Date):
            self.LastDate = Date
        self.Hours += Hours
        self.Flights += 1

# Trips is the only class that is populated after the logbook there for the constructor must recieve values for members (Miles,Hours,Date)
class Trips(object):
    Miles = 0
    Flights = 0
    Hours = 0
    FirstDate = None
    LastDate = None
    RevFlights = 0
    RevHours = 0
    RevFirstDate = None
    RevLastDate = None

    def __init__(self,Date,Hours,Miles):
        self.Miles=Miles
        self.Flights = 1
        self.RevFlights = 0
        self.Hours = Hours
        self.FirstDate = Date
        self.LastDate = Date

    def __repr__(self):
        return str([self.Hours,self.Flights,self.Miles,self.FirstDate,self.LastDate,self.RevFlights,self.RevFirstDate,self.RevLastDate])

    def addTrip(self,Date,Hours):
        self.Flights += 1
        self.Hours += Hours
        if (self.LastDate < Date):
            self.LastDate = Date
        if (self.FirstDate > Date):
            self.FirstDate = Date
    def addRevTrip(self,Date,Hours):
        self.RevFlights += 1
        self.RevHours += Hours
        if self.RevLastDate == None or (self.RevLastDate < Date):
            self.RevLastDate = Date
        if self.RevFirstDate == None or (self.RevFirstDate > Date):
            self.RevFirstDate = Date
