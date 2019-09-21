from django.urls import include, path
from . import views, pushMessage

# 用來串接callback主程式
urlpatterns = [
    path('callback/', views.callback),
    path('pushMessage/', pushMessage.pushView.as_view(), name="pushMessage"),
]