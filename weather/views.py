import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
from django.contrib import messages

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=0cd7fdcef004e49548354e3d54c04578'
    if request.method == 'POST':
        form = CityForm(request.POST)
        err_mess = ''
        if form.is_valid():
            current_city = form.cleaned_data['name'] 
            exist_city = City.objects.filter(name=current_city).count()
            if exist_city==0:
                re = requests.get(url.format(current_city)).json()
                if re['cod'] ==200:
                   form.save()
                   
                else:
                    messages.info(request, f" name is not a valid city name") 

            else:
                messages.info(request, f" This city already exist")
              
        
    form = CityForm()

    cities = City.objects.all()


    weather_dic = []

    for city in cities:

        
        re = requests.get(url.format(city)).json()
        print(re)
        

        city_weather = {
            'city' : city.name,
            'temperature' : re['main']['temp'],
            'description' : re['weather'][0]['description'],
            'Pressure' : re['main']['pressure'],
            'humidity' : re['main']['humidity'],
            'icon' : re['weather'][0]['icon'],
        }

        weather_dic.append(city_weather)

    context = {'weather_data' : weather_dic, 'form' : form}
    return render(request, 'weather/weather.html', context)

def remove_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')
