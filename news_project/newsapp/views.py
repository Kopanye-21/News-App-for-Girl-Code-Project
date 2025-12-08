import requests
from django.conf import settings
from django.shortcuts import render
from django.utils.html import mark_safe
from .models import Advertisement
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import redirect
from .forms import ArticleForm

#  Create your views here.
GNEWS_BASE = 'https://gnews.io/api/v4' 
WEATHER_BASE = 'https://api.openweathermap.org/data/2.5/weather'

def fetch_news(endpoint, params): 
    params['token'] = settings.GNEWS_API_KEY 
    try: 
            r = requests.get(f'{GNEWS_BASE}/{endpoint}', params=params, timeout=8) 
            r.raise_for_status() 
            return r.json().get('articles', []) 
    except Exception: return []

def get_weather_for(city='Johannesburg'): 
    key = settings.OPENWEATHER_API_KEY 
    if not key: 
        return None 
    params = {'q': city, 'appid': key, 'units': 'metric'}
    try: 
        r = requests.get(WEATHER_BASE, params=params, timeout=6) 
        r.raise_for_status() 
        data = r.json() 
        return { 'city': data.get('name'), 'temp': data['main']['temp'], 'desc': data['weather'][0]['description'].capitalize(), } 
    except Exception: return None

def home(request): 
    articles = fetch_news('top-headlines', {'lang': 'en'}) 
    weather = get_weather_for() 
    return render(request, 'newsapp/home.html', {'articles': articles, 'weather': weather})

def category(request, cat):
      # GNews topics: world, nation, business, technology, entertainment, sports, science, health 
        articles = fetch_news('top-headlines', {'lang': 'en', 'topic': cat})
        weather = get_weather_for() 
        return render(request, 'newsapp/category.html', {'articles': articles, 'cat': cat.title(), 'weather': weather})

def search(request): 
    q = request.GET.get('q', '').strip() 
    articles = [] 
    if q: 
        articles = fetch_news('search', {'q': q, 'lang': 'en', 'max': 30}) 
        weather = get_weather_for() 
        return render(request, 'newsapp/search_results.html', {'articles': articles, 'query': q, 'weather': weather})
    
def home(request): 
    adds = Advertisement.objects.all()
    articles = fetch_news('top-headlines', {'lang': 'en'})    
    weather = get_weather_for()
    return render(request, 'newsapp/home.html', {'articles': articles, 'weather': weather, 'adds': adds})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # auto login
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'auth/signup.html', {'form': form})

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('newsapp:home') # redirect after saving
    else:
        form = ArticleForm()
    return render(request, 'newsapp/add_article.html', {'form': form})