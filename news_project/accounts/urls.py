from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    #path('account/signup/', views.signup_view, name='signup'),
]