from django.http import HttpResponse
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=008ba8da75e37370edaa4de0e74d5931'

    err_msg=''
    if request.method == 'POST':
        form =CityForm(request.POST)
        
        if form.is_valid():
            new_city=form.cleaned_data['name']
            countt=City.objects.filter(name=new_city).count()

            if countt==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_msg='City is invalid'
            else:
                err_msg ='City is already added!!!'

    form =CityForm()
    cities = City.objects.all()
    weather_data=[]
    for city in cities:
        r=requests.get(url.format(city)).json()

        city_weather ={
            'city': city.name ,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'] ,
            'icon':r['weather'][0]['icon'] ,
        }
        weather_data.append(city_weather)
    
    context ={'weather_data':weather_data,'form':form}
    return render(request,'weather.html',context)