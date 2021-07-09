"""beautyproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import UserCreationView, ProductList
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.Base, name='Base'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='Accedi'),
    path('register/', UserCreationView.as_view(), name='Registration'),
    path('logout/', views.logout_view, name='Logout'),
    path('profile/', views.Profile, name='Profile'),
    path('search_bar/', views.SearchBar, name='SearchBar'),
    path('search_bar/<int:pk>/products_list/', ProductList.as_view(), name='ProductList'),
    path('change-password/', views.change_password, name='change_password'),
] + static(settings.STATIC_URL)