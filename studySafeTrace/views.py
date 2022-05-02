from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.

subject = "COMP3297"
date = datetime.datetime.now()
contacts=["Lok, Wing Ching","Yip, Yau Shing","Loo, Chi Nan","Chai, Wun Ching","Cheung, Ka Chun"]
venues=["K.K. Leung Building, Main Campus","Main Building, Main Campus","Centennial Campus, Central Podium Levels - Two","Main Campus, T.T. Tsui Building"]


def contact_view(request):
    return render(request, 'contacts.html',{"subject":subject,"date":date,"contacts":contacts})

def venue_view(request):
    return render(request, 'venues.html',{"subject":subject,"date":date,"venues":venues})

def base_view(request):
    return render(request, 'base.html',{"subject":subject,"date":date})
