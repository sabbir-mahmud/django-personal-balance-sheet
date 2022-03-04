# imports
from django.contrib import admin
from django.urls import path, include
from . import views

# urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('history.urls')),
    path('login/', views.login_view, name='login'),
]
