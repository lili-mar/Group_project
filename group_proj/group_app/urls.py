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
    path('myEvents', views.myEvents),
    path('dashboard', views.dashboard),
    path('newJoin', views.newJoin),
    path('confirmJoin', views.confirmJoin),


]
