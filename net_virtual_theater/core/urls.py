from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.join_watch_party, name='join_watch_party'),
    path('leavewatchparty/', views.leave_watch_party, name='leave_watch_party'),
]
