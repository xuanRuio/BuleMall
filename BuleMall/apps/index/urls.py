from django.urls import path
from apps.index import views

app_name = 'index'

urlpatterns = [
    path('', views.IndexView.as_view(),name='index_page'),
]
