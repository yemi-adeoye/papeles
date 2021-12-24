from django.urls import path, utils
from . import views

app_name = 'news'

# app specific url patterns
urlpatterns = [
    path('', views.home, name='home'),
    path('keywords', views.get_keywords, name='get_keywords'),
    path('set-keywords', views.update_keywords, name='update_keywords'),
    path('<str:paper>', views.get_news, name='get_news'),

]
