from django.urls import include, path
from . import views

# 用來串接callback主程式
urlpatterns = [
    path('', views.pushView.as_view(), name="pushMessage"),
]