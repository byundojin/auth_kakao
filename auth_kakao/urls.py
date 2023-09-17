from django.urls import path
from . import views

urlpatterns = [
    path("authorize_code", views.get_authorize_code),
    path("callback", views.callback)
]
