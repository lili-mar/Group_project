from django.urls import path     
from . import views
urlpatterns = [
    
    #call it as http://localhost:8000/ABC/
    path('', views.index),	
    
       
]
