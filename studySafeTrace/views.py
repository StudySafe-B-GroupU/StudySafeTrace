from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
import json
import requests

# Create your views here.

records_json = {"resource":"https://blooming-badlands-56728.herokuapp.com/api/records","section":1,"format":"json","filters":[[1,"eq",["event"]]]}
records_obj_json = json.dumps(records_json)
records_resp = requests.get("https://blooming-badlands-56728.herokuapp.com/api/records", params={'q': records_obj_json})
records_result = records_resp.json()


#subject = HttpRequest.GET["subject"]
#date = HttpRequest.GET["date"]

record_entry=[]
record_exit=[]


def contact_view(request):
    subject = request.GET["subject"]
    date = request.GET["date"]
    contacts=listOutContact(subject,date)
    return render(request, 'contacts.html',{"subject":subject,"date":date,"contacts":contacts})

def venue_view(request):
    subject = request.GET["subject"]
    date = request.GET["date"]
    venues=listOutVenue(subject,date)
    return render(request, 'venues.html',{"subject":subject,"date":date,"venues":venues})

def base_view(request):
    subject = request.GET["subject"]
    date = request.GET["date"]
    return render(request, 'base.html',{"subject":subject,"date":date})

def listOutVenue(subject,date):
    for record in records_result:
        if(record["event"]=="Entry"):
            record_entry.append(record)
        elif(record["event"]=="Exit"):
            record_exit.append(record)

    entryList=[]
    for record_en in record_entry:
        entryDict={}
        entryDay = ""
        entryTime = ""
        for i in range(len(record_en["date_time"])):
            if(i<10):
                entryDay+=record_en["date_time"][i]
            if(i>10 and i<19):
                entryTime+=record_en["date_time"][i]
        entryDict["hku_id"]=record_en["hku_id"]
        entryDict["venueCode"]=record_en["venueCode"]
        entryDict["entryDay"]=entryDay
        entryDict["entryTime"]=entryTime
        entryList.append(entryDict)

    exitList=[]
    for record_ex in record_exit:
        exitDict={}
        exitDay = ""
        exitTime = ""
        for i in range(len(record_ex["date_time"])):
            if(i<10):
                exitDay+=record_ex["date_time"][i]
            if(i>10 and i<19):
                exitTime+=record_ex["date_time"][i]
        exitDict["hku_id"]=record_ex["hku_id"]
        exitDict["venueCode"]=record_ex["venueCode"]
        exitDict["exitDay"]=exitDay
        exitDict["exitTime"]=exitTime
        exitList.append(exitDict)

    matchList=[]
    for dict_en in entryList:
        for dict_ex in exitList:
            matchDict={}


            entryTime_split = dict_en["entryTime"].split(":")
            entryHour = int(entryTime_split[0])
            entryMin = int(entryTime_split[1])
            entrySec = int(entryTime_split[2])
            exitTime_split = dict_ex["exitTime"].split(":")
            exitHour=int(exitTime_split[0])
            exitMin=int(exitTime_split[1])
            exitSec=int(exitTime_split[2])

            comHour=exitHour-entryHour
            if(exitMin<entryMin):
                comHour-=1
                comMin=exitMin+60-entryMin
            else:
                comMin=exitMin-entryMin
            if(exitSec<entrySec):
                comMin-=1
                comSec=exitSec+60-entrySec
            else:
                comSec=exitSec-entrySec

            comHour=str(comHour)
            comMin=str(comMin)
            comSec=str(comSec)
            if(len(comHour)==1):
                comHour="0"+comHour
            if(len(comMin)==1):
                comMin="0"+comMin
            if(len(comSec)==1):
                comSec="0"+comSec

            duration = comHour+":"+comMin+":"+comSec

            if(dict_en["hku_id"]==dict_ex["hku_id"] and dict_en["venueCode"]==dict_ex["venueCode"] and dict_en["entryDay"]==dict_ex["exitDay"] ):
                matchDict["hku_id"]=dict_en["hku_id"]
                matchDict["venueCode"]=dict_en["venueCode"]
                matchDict["entryDay"]=dict_en["entryDay"]
                matchDict["entryTime"]=dict_en["entryTime"]
                matchDict["duration"]=duration
                dict_en["entryDay"]="used_en"
                dict_ex["exitDay"]="used_ex"
                matchList.append(matchDict)

    #demo
    date_split = date.split("-")
    end_year = int(date_split[0])
    end_month = int(date_split[1])
    end_day = int(date_split[2])
    if(end_day<=2):
        if(end_month==1):
            if(end_day ==1):
                start_month = 12
                start_year = end_year-1
                mid_month = 12
                mid_year = end_year -1
            else:
                start_month=12
                start_year = end_year-1
                mid_month = end_month
                mid_year = end_year
        else:
            if(end_day ==1):
                start_month = end_month-1
                start_year = end_year
                mid_month = end_month-1
                mid_year = end_year
            else:
                start_month=end_month-1
                start_year = end_year
                mid_month = end_month
                mid_year = end_year
        if(start_month==1 or start_month==3 or start_month==5 or start_month==7 or start_month==8 or start_month==10 or start_month==12):
            if(end_day==2):
                start_day=31
                mid_day = 1
            if(end_day==1):
                start_day=30
                mid_day = 31
        elif(start_month==4 or start_month==6 or start_month==9 or start_month==11):
            if(end_day==2):
                start_day=30
                mid_day = 1
            if(end_day==1):
                start_day=29
                mid_day = 30
        elif(start_month==2):
            if((end_year%4)==0):
                if(end_day==2):
                    start_day=29
                    mid_day = 1
                if(end_day==1):
                    start_day=28
                    mid_day = 29
            else:
                if(end_day==2):
                    start_day=28
                    mid_day = 1
                if(end_day==1):
                    start_day=27
                    mid_day = 28
    else:
        start_day = end_day-2
        start_month = end_month
        start_year = end_year
        mid_day = end_day-1
        mid_month = end_month
        mid_year = end_year
    if(start_day<10):
        start_day="0"+str(start_day)
    if(start_month<10):
        start_month="0"+str(start_month)
    if(mid_day<10):
        mid_day="0"+str(mid_day)
    if(mid_month<10):
        mid_month="0"+str(mid_month)
    if(end_day<10):
        end_day="0"+str(end_day)
    if(end_month<10):
        end_month="0"+str(end_month)

    start_date=str(start_year)+"-"+str(start_month)+"-"+str(start_day)
    mid_date=str(mid_year)+"-"+str(mid_month)+"-"+str(mid_day)
    end_date=str(end_year)+"-"+str(end_month)+"-"+str(end_day)

    contacts=[]
    venues=[]

    stamp=[]
    for visit in matchList:
        day_time={}
        place_time={}
        if(subject == visit["hku_id"]):
            if(start_date == visit["entryDay"] or mid_date == visit["entryDay"] or end_date == visit["entryDay"]):
                venues.append(visit["venueCode"])
                stamp.append(visit["venueCode"])
                stamp.append(visit["entryDay"])
                stamp.append(visit["entryTime"])


    venues=list( dict.fromkeys(venues))



    stamp_venue=[]
    stamp_day=[]
    stamp_time=[]
    for place in range(0,len(stamp),3):
        if(len(stamp_venue)==0):
            stamp_venue.append(stamp[place])
            stamp_day.append(stamp[place+1])
            stamp_time.append(stamp[place+2])
        else:
            for i in range(len(stamp_venue)):
                if(stamp[place] in stamp_venue):
                    check=True
                    break
                check=False

            if(check):
                check=False
            else:
                stamp_venue.append(stamp[place])
                stamp_day.append(stamp[place+1])
                stamp_time.append(stamp[place+2])

    for count in range(len(stamp_venue)):
        oDate_split = stamp_day[count].split("-")
        oYear = int(oDate_split[0])
        oMonth = int(oDate_split[1])
        oDay = int(oDate_split[2])
        oTime_split = stamp_time[count].split(":")
        oHour = int(oTime_split[0])
        oMin = int(oTime_split[1])
        oSec = int(oTime_split[2])
        for record in matchList:

            tDate_split = record["entryDay"].split("-")
            tYear = int(tDate_split[0])
            tMonth = int(tDate_split[1])
            tDay = int(tDate_split[2])
            tTime_split = record["entryTime"].split(":")
            tHour = int(tTime_split[0])
            tMin = int(tTime_split[1])
            tSec = int(tTime_split[2])

            rDuration_split=record["duration"].split(":")
            rHour = int(rDuration_split[0])
            rMin = int(rDuration_split[1])
            rDuration = rHour*60+rMin

            if(record["venueCode"]==stamp_venue[count] and (tYear>=oYear and tMonth>=oMonth and tDay>=oDay) and (tHour>=oHour and tMin>=oMin and tSec>=oSec) and rDuration>=30):
                contacts.append(record["hku_id"])

    contacts=list( dict.fromkeys(contacts))
    contacts.remove(subject)
    venues = sorted(venues)
    return venues

def listOutContact(subject,date):
    for record in records_result:
        if(record["event"]=="Entry"):
            record_entry.append(record)
        elif(record["event"]=="Exit"):
            record_exit.append(record)

    entryList=[]
    for record_en in record_entry:
        entryDict={}
        entryDay = ""
        entryTime = ""
        for i in range(len(record_en["date_time"])):
            if(i<10):
                entryDay+=record_en["date_time"][i]
            if(i>10 and i<19):
                entryTime+=record_en["date_time"][i]
        entryDict["hku_id"]=record_en["hku_id"]
        entryDict["venueCode"]=record_en["venueCode"]
        entryDict["entryDay"]=entryDay
        entryDict["entryTime"]=entryTime
        entryList.append(entryDict)

    exitList=[]
    for record_ex in record_exit:
        exitDict={}
        exitDay = ""
        exitTime = ""
        for i in range(len(record_ex["date_time"])):
            if(i<10):
                exitDay+=record_ex["date_time"][i]
            if(i>10 and i<19):
                exitTime+=record_ex["date_time"][i]
        exitDict["hku_id"]=record_ex["hku_id"]
        exitDict["venueCode"]=record_ex["venueCode"]
        exitDict["exitDay"]=exitDay
        exitDict["exitTime"]=exitTime
        exitList.append(exitDict)

    matchList=[]
    for dict_en in entryList:
        for dict_ex in exitList:
            matchDict={}


            entryTime_split = dict_en["entryTime"].split(":")
            entryHour = int(entryTime_split[0])
            entryMin = int(entryTime_split[1])
            entrySec = int(entryTime_split[2])
            exitTime_split = dict_ex["exitTime"].split(":")
            exitHour=int(exitTime_split[0])
            exitMin=int(exitTime_split[1])
            exitSec=int(exitTime_split[2])

            comHour=exitHour-entryHour
            if(exitMin<entryMin):
                comHour-=1
                comMin=exitMin+60-entryMin
            else:
                comMin=exitMin-entryMin
            if(exitSec<entrySec):
                comMin-=1
                comSec=exitSec+60-entrySec
            else:
                comSec=exitSec-entrySec

            comHour=str(comHour)
            comMin=str(comMin)
            comSec=str(comSec)
            if(len(comHour)==1):
                comHour="0"+comHour
            if(len(comMin)==1):
                comMin="0"+comMin
            if(len(comSec)==1):
                comSec="0"+comSec

            duration = comHour+":"+comMin+":"+comSec

            if(dict_en["hku_id"]==dict_ex["hku_id"] and dict_en["venueCode"]==dict_ex["venueCode"] and dict_en["entryDay"]==dict_ex["exitDay"] ):
                matchDict["hku_id"]=dict_en["hku_id"]
                matchDict["venueCode"]=dict_en["venueCode"]
                matchDict["entryDay"]=dict_en["entryDay"]
                matchDict["entryTime"]=dict_en["entryTime"]
                matchDict["duration"]=duration
                dict_en["entryDay"]="used_en"
                dict_ex["exitDay"]="used_ex"
                matchList.append(matchDict)

    #demo
    date_split = date.split("-")
    end_year = int(date_split[0])
    end_month = int(date_split[1])
    end_day = int(date_split[2])
    if(end_day<=2):
        if(end_month==1):
            if(end_day ==1):
                start_month = 12
                start_year = end_year-1
                mid_month = 12
                mid_year = end_year -1
            else:
                start_month=12
                start_year = end_year-1
                mid_month = end_month
                mid_year = end_year
        else:
            if(end_day ==1):
                start_month = end_month-1
                start_year = end_year
                mid_month = end_month-1
                mid_year = end_year
            else:
                start_month=end_month-1
                start_year = end_year
                mid_month = end_month
                mid_year = end_year
        if(start_month==1 or start_month==3 or start_month==5 or start_month==7 or start_month==8 or start_month==10 or start_month==12):
            if(end_day==2):
                start_day=31
                mid_day = 1
            if(end_day==1):
                start_day=30
                mid_day = 31
        elif(start_month==4 or start_month==6 or start_month==9 or start_month==11):
            if(end_day==2):
                start_day=30
                mid_day = 1
            if(end_day==1):
                start_day=29
                mid_day = 30
        elif(start_month==2):
            if((end_year%4)==0):
                if(end_day==2):
                    start_day=29
                    mid_day = 1
                if(end_day==1):
                    start_day=28
                    mid_day = 29
            else:
                if(end_day==2):
                    start_day=28
                    mid_day = 1
                if(end_day==1):
                    start_day=27
                    mid_day = 28
    else:
        start_day = end_day-2
        start_month = end_month
        start_year = end_year
        mid_day = end_day-1
        mid_month = end_month
        mid_year = end_year
    if(start_day<10):
        start_day="0"+str(start_day)
    if(start_month<10):
        start_month="0"+str(start_month)
    if(mid_day<10):
        mid_day="0"+str(mid_day)
    if(mid_month<10):
        mid_month="0"+str(mid_month)
    if(end_day<10):
        end_day="0"+str(end_day)
    if(end_month<10):
        end_month="0"+str(end_month)

    start_date=str(start_year)+"-"+str(start_month)+"-"+str(start_day)
    mid_date=str(mid_year)+"-"+str(mid_month)+"-"+str(mid_day)
    end_date=str(end_year)+"-"+str(end_month)+"-"+str(end_day)

    contacts=[]
    venues=[]

    stamp=[]
    for visit in matchList:
        day_time={}
        place_time={}
        if(subject == visit["hku_id"]):
            if(start_date == visit["entryDay"] or mid_date == visit["entryDay"] or end_date == visit["entryDay"]):
                venues.append(visit["venueCode"])
                stamp.append(visit["venueCode"])
                stamp.append(visit["entryDay"])
                stamp.append(visit["entryTime"])


    venues=list( dict.fromkeys(venues))



    stamp_venue=[]
    stamp_day=[]
    stamp_time=[]
    for place in range(0,len(stamp),3):
        if(len(stamp_venue)==0):
            stamp_venue.append(stamp[place])
            stamp_day.append(stamp[place+1])
            stamp_time.append(stamp[place+2])
        else:
            for i in range(len(stamp_venue)):
                if(stamp[place] in stamp_venue):
                    check=True
                    break
                check=False

            if(check):
                check=False
            else:
                stamp_venue.append(stamp[place])
                stamp_day.append(stamp[place+1])
                stamp_time.append(stamp[place+2])

    for count in range(len(stamp_venue)):
        oDate_split = stamp_day[count].split("-")
        oYear = int(oDate_split[0])
        oMonth = int(oDate_split[1])
        oDay = int(oDate_split[2])
        oTime_split = stamp_time[count].split(":")
        oHour = int(oTime_split[0])
        oMin = int(oTime_split[1])
        oSec = int(oTime_split[2])
        for record in matchList:

            tDate_split = record["entryDay"].split("-")
            tYear = int(tDate_split[0])
            tMonth = int(tDate_split[1])
            tDay = int(tDate_split[2])
            tTime_split = record["entryTime"].split(":")
            tHour = int(tTime_split[0])
            tMin = int(tTime_split[1])
            tSec = int(tTime_split[2])

            rDuration_split=record["duration"].split(":")
            rHour = int(rDuration_split[0])
            rMin = int(rDuration_split[1])
            rDuration = rHour*60+rMin

            if(record["venueCode"]==stamp_venue[count] and (tYear>=oYear and tMonth>=oMonth and tDay>=oDay) and (tHour>=oHour and tMin>=oMin and tSec>=oSec) and rDuration>=30):
                contacts.append(record["hku_id"])

    contacts=list( dict.fromkeys(contacts))
    contacts.remove(subject)

    contacts=sorted(contacts)

    return contacts
