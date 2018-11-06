from django.contrib import admin
from django.urls import include, path
from money import views


urlpatterns = [
    path(r'monthlysum/', views.MonthlySumView.as_view()),
    path(r'monthlybillinfo/', views.MonthlybillInfoView.as_view()),
    path(r'accountbalance/', views.AccountBalanceView.as_view()),

]