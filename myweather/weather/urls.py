from django.urls import path,include
from weather import views

urlpatterns = [
    path('',views.index,name='index'),
]