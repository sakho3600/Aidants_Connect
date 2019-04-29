from django.urls import path
from aidants_connect_web import views

urlpatterns = [path("authorize/", views.authorize, name="authorize"),
               path("token/", views.token, name="token"),
               ]
