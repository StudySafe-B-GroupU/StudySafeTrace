from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
# Create your views here.

records_json = {"resource":"https://blooming-badlands-56728.herokuapp.com/api/records","section":1,"format":"json","filters":[[1,"eq",["event"]]]}
records_obj_json = json.dumps(records_json)
records_resp = requests.get("https://blooming-badlands-56728.herokuapp.com/api/records", params={'q': records_obj_json})
records_result = records_resp.json()
record_entry=[]
record_exit=[]
footprint_id=[]
footprint_place=[]

for record in records_result:
    if(record["event"]=="Entry"):
        record_entry.append(record)
for record_en in record_entry:
    time_place = {}
    id_footprint = {}
    time_id = {}
    place_footprint={}
    hku_id = record_en["hku_id"]
    venueCode = record_en["venueCode"]
    entryDay = ""
    for i in range(len(record_en["date_time"])):
        if(i<10):
            entryDay+=record_en["date_time"][i]
    time_place[entryDay]=venueCode
    id_footprint[hku_id]=time_place
    time_id[entryDay]=hku_id
    place_footprint[venueCode]=time_id

    footprint_id.append(id_footprint)
    footprint_place.append(place_footprint)



subject = '3025704501'
date = "2022-05-05"
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
visit_footprint=[]
for visit in footprint_id:
    if(subject in visit):
        if(start_date in visit[subject]):
            venues.append(visit[subject][start_date])
            visit_footprint.append(visit[subject])
        elif(mid_date in visit[subject]):
            venues.append(visit[subject][mid_date])
        elif(end_date in visit[subject]):
            venues.append(visit[subject][end_date])
venues=list( dict.fromkeys(venues))

for place in venues:
    for meet in footprint_place:
        if(place in meet):
            if(start_date in meet[place]):
                contacts.append(meet[place][start_date])
            elif(mid_date in meet[place]):
                contacts.append(meet[place][mid_date])
            elif(end_date in meet[place]):
                contacts.append(meet[place][end_date])

contacts=list( dict.fromkeys(contacts))

print(contacts)


def contact_view(request):
    return render(request, 'contacts.html',{"subject":subject,"date":date,"contacts":contacts})

def venue_view(request):
    return render(request, 'venues.html',{"subject":subject,"date":date,"venues":venues})

def base_view(request):
    return render(request, 'base.html',{"subject":subject,"date":date})
