from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.registration, name="register"),
    path('register/', views.register),
    path('message_display_home/', views.message_display_home, name="message_display_home"),
    path('message_display_dashboard/', views.message_display_dashboard, name="message_display_dashboard"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('list/', views.list, name="list"),
    path('count_avg/', views.count_avg, name="count_avg"),
    path('count_total/', views.count_total, name="count_total"),
    path('add_user/', views.add_user_page, name="add_user"),
    path('list_all/', views.list_all, name="list all"),
    path('cluster/', views.list_clu, name="list cluster"),
    path('count_total_P/', views.count_total_P, name="list total POSITIVE"),
    path('count_avg_P/', views.count_avg_P, name="list avg POSITIVE"),
]