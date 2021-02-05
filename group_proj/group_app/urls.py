from django.urls import path
from . import views

urlpatterns = [

    # REMEMBER to call it as http://localhost:8000/ABC/

    path('', views.index),  # display login
    path('login', views.login),  # process/validate login

    path('regForm', views.regForm),  # display regForm
    path('register', views.register),  # validate registration

    path('logout', views.logout),

    path('childForm', views.childForm),  # display childForm
    path('regChild', views.regChild),  # validate registration for a Child

    path('myProfile', views.myProfile),

    path('update_myProfile', views.update_myProfile,
         name='update_myProfile'),  # update myProfile

    path('remove_child_myProfile', views.remove_child_myProfile,
         name='remove_child_myProfile'),  # remove child from myProfile


    # ---------Here we are.  We still need the below pages to work------------------------------------------

    path('remove_event_myEvents', views.remove_event_myEvents,
         name='remove_event_myEvents'),  # remove event from myEvents

    path('myEvents', views.myEvents),
    path('dashboard', views.dashboard),
    path('event/<int:event_id>/newJoin', views.newJoin),



    #path('confirmJoin', views.confirmJoin),
    # localhost:8000/ABC/<event_id/confirmJoin>
    path('<int:event_id>/confirmJoin', views.confirmJoin),
    path('<int:event_id>/createMessage', views.create_msg),
    path('createComment/<int:msg_id>', views.create_comment),
    path('delete/<int:comm_id>', views.delete_comment),
    path('like/<int:msg_id>', views.add_like),
    path('unlike/<int:msg_id>', views.remove_like),


]
