from django.urls import include, path
from . import views, mod

# 用來串接callback主程式
urlpatterns = [
    path('callback/', views.callback),
    path('dataBase/', mod.dataBaseView.as_view(), name="dataBase"),
    path('pushMessage/', mod.pushMessageView.as_view(), name="pushMessage"),
    path('jsonData/<str:tableName>/', mod.getJSON),
]