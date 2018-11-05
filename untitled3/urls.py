"""untitled3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from api import views


urlpatterns = [
    path(r'admin/', admin.site.urls),
    # path(r'base/ecs/', include(('ecs.urls', 'ecs'), namespace='ecs')),
    path(r'api/v1/money/', include(('money.urls', 'money'), namespace='money')),
    # path(r'base/rds/', include('rds.urls')),
    # path(r'base/other/', include('other.urls')),
    # path(r'api/v1/auth/', views.AuthView.as_view()),
    # path(r'api/v1/monthlybill/', views.MonthlyBillView.as_view()),
    # path(r'api/v1/monthlyinstanceconsumption/', views.MonthlyInstanceConsumptionView.as_view())
    # path(r'api/v1/accountbalance/', views.AccountBalanceView.as_view()),
    path(r'api/v1/availableinstances/', views.AvailableInstancesView.as_view())
]
