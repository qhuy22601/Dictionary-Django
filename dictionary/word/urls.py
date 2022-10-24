from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('migration-data', views.migration_data_word, name='test'),
    path('find-sentence-by-word/<str:word>', views.findSentenceByWord, name='findSentenceByWord'),
]