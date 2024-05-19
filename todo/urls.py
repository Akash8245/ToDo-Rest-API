
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome user !")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ),
    path('api/',include('api.urls')),
]
