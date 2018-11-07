from django.contrib import admin
from django.urls import include, path
from money import views


urlpatterns = [
    #每月不同业务线和环境消费总览情况
    path(r'monthlysum/', views.MonthlySumView.as_view()),
    #每月不同业务线和环境消费明细
    path(r'monthlybillinfo/', views.MonthlybillInfoView.as_view()),
    #阿里云账号剩余可用金额
    path(r'accountbalance/', views.AccountBalanceView.as_view()),
    #ECS实例
    path(r'ecsinfo/', views.EcsInfoView.as_view()),
    # path(r'ecsinfo/<int:pk>/', views.EcsInfoIdView.as_view(), name='ecsinfo-id'),
    #RDS实例
    path(r'rdsinfo/', views.RdsInfoView.as_view()),
    #SLB实例
    path(r'slbinfo/', views.SlbInfoView.as_view()),
    #EIP实例
    path(r'eipinfo/', views.EipInfoView.as_view()),
]