from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('migration-data', views.migration_data_word, name='test'),
    path('words/<str:word>', views.findSentenceByWord, name='findSentenceByWord'),
    path('hihi', views.hihi),
    path('home', views.home),
]