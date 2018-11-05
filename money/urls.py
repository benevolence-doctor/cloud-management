from django.contrib import admin
from django.urls import include, path
from money import views


urlpatterns = [
    path(r'monthlybill/', views.MonthlyBillView.as_view()),
    path(r'monthlysum/', views.MonthlySumView.as_view()),
    path(r'accountbalance/', views.AccountBalanceView.as_view()),

]