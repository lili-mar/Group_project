from django.urls import path
from . import views

urlpatterns = [

    # REMEMBER to call it as http://localhost:8000/ABC/

    #path('', views.maptest),
    path('', views.index),  # display login
    path('login', views.login),  # process/validate login

    path('regForm', views.regForm),  # display regForm
    path('register', views.register),  # validate registration

    path('logout', views.logout),

    # ---------from here down -we need to work on the programming/development.  We also need to finish the models.py---------------
    # I think there should be an Event model and a Child model -but we can discuss

    path('childForm', views.childForm),  # display childForm
    path('regChild', views.regChild),  # validate registration for a Child

    path('myProfile', views.myProfile),
    
    path('update_myProfile', views.update_myProfile,
         name='update_myProfile'),  # update myProfile

    path('remove_child_myProfile', views.remove_child_myProfile,
         name='remove_child_myProfile'),  # remove child from myProfile

    path('remove_event_myEvents', views.remove_event_myEvents,
         name='remove_event_myEvents'),  # remove event from myEvents 
    
    path('myEvents', views.myEvents),
    path('dashboard', views.dashboard),
    path('event/<int:id>/newJoin', views.newJoin),
    path('confirmJoin', views.confirmJoin),


]
