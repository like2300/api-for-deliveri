from django.urls import path
from . import views

urlpatterns = [
    path('init-app-data/', views.init_app_data_view, name='init-app-data'),
]