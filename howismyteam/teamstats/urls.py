from django.urls import path
from . import views

app_name = 'teamstats'

urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login_view'),
    path('logout', views.UserLogoutView.as_view(), name='logout_view'),
    path('poll', views.UserPollView.as_view(), name='userpoll_view'),
    path('results', views.ResultsView.as_view(), name='results_view'),
]
