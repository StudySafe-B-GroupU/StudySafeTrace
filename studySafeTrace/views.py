from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from datetime import date, timedelta
# Create your views here.

filter_date=date.today()
data_Quarantine_centres=data_Capunit=[]
data_usedunit=data_PIU=data_avause=data_nonclose=0
data_consistent=False
data_date=''
sort_centres = {}
sorted_centre = []

def run(fdates):
    global data_Quarantine_centres,data_Capunit,data_usedunit,data_PIU,data_avause,data_consistent,data_date,data_nonclose,connection_status,data_status,sort_centres,sorted_centre
    dates=fdates.strftime('%d/%m/%Y')

    #in centre
    centre_json = {"resource":"http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv","section":1,"format":"json","filters":[[1,"eq",[dates]]]}
    centre_obj_json = json.dumps(centre_json)
    centre_resp = requests.get("https://api.data.gov.hk/v2/filter", params={'q': centre_obj_json})
    centre_result = centre_resp.json()

    #number of types
    types_json = {"resource":"http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv","section":1,"format":"json","filters":[[1,"eq",[dates]]]}
    types_obj_json = json.dumps(types_json)
    types_resp = requests.get("https://api.data.gov.hk/v2/filter", params={'q': types_obj_json})
    types_result = types_resp.json()

    if(centre_result==[] or types_result==[]):
        newdate=fdates- timedelta(days = 1)
        if((filter_date.day-newdate.day) == 8):
            data_status = False
        else:
            run(newdate)
    else:
        data_date=dates
        for i in centre_result:
            data_Quarantine_centres.append(i['Quarantine centres'])
            data_Capunit.append(i['Capacity (unit)'])
            data_usedunit+=int(i['Current unit in use'])
            data_PIU+=int(i['Current person in use'])
            data_avause+=int(i['Ready to be used (unit)'])
            sort_centres.update({i['Quarantine centres']:i['Capacity (unit)']})
        sort_centres= sorted(sort_centres.items(), key=lambda x: x[1], reverse=True)
        sort_centres = dict((x, y) for x, y in sort_centres)
        count=0
        for u in sort_centres:
            if(count<3):
                sorted_centre.append({"name":u,"units":str(sort_centres[u])})
                count+=1
        data_nonclose = types_result[0]['Current number of non-close contacts']
        if(data_PIU== (int(types_result[0]['Current number of close contacts of confirmed cases'])+data_nonclose)):
            data_consistent = True
        else:
            data_consistent = False
        connection_status = (centre_resp.ok and types_resp.ok)
        data_status = True



def view(request):
    global data_Quarantine_centres,data_Capunit,data_usedunit,data_PIU,data_avause,data_consistent,data_date,data_nonclose,connection_status,data_status,sort_centres,sorted_centre
    run(filter_date)
    data = {
    "date": data_date,
    "units_in_use": data_usedunit,
    "units_available": str(data_avause),
    "persons_quarantined": str(data_PIU),
    "non_close_contacts": str(data_nonclose),
    "count_consistent": data_consistent
    }
    centres = sorted_centre
    connected = connection_status
    #"connected" : connection_status,
    #"has_data" : data_status
    has_data = data_status

    data_Quarantine_centres=data_Capunit=[]
    data_usedunit=data_PIU=data_avause=data_nonclose=0
    data_consistent=False
    data_date=''
    sort_centres = {}
    sorted_centre = []

    return render(request, 'dashboard3.html', {"data":data,"connected":connected,"has_data":has_data,"centres":centres})
