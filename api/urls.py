
from django.contrib import admin
from django.urls import path
from .views import Register,Login,getSetTask,updateTask,deleteTask

urlpatterns = [
    path('register/',Register.as_view()),
    path('login/',Login.as_view()),
    path('task/',getSetTask.as_view()),
    path('task/update/<int:pk>',updateTask.as_view()),
    path('task/delete/<int:pk>',deleteTask.as_view()),
]
