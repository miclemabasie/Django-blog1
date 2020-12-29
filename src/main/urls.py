from django.urls import path
from .views import home, about, contact

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact')
]
