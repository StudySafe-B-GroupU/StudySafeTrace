from django.urls import path
from studySafeTrace import views

urlpatterns = [
    path('contacts/',views.contact_view),
    path('venues/',views.venue_view),
    path('',views.base_view),
]
