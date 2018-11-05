# -*- coding: utf8 -*-
'''
按照业务线和环境将实例总消费信心存储到数据库
'''
import os
import sys
import json
import math

# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from django.db.models import Sum
from api.models import  MonthlybillInfo, MonthlySum
from django.conf import settings

def get_monthly_sum(business_line, env, billingCycle):

    try:
        result_sum = MonthlybillInfo.objects.filter(businessLine=business_line, env=env, billingCycle=billingCycle).values(
            'productName').annotate(sum=Sum('pretaxAmount')).values('billingCycle','productName','sum')
        print (result_sum)
    except Exception as e:
        print (e)

    for item in result_sum:
        try:
            MonthlySum.objects.get(businessLine=business_line, env=env,
                                   billingCycle=billingCycle, productName=item.get('productName'))
        except MonthlySum.DoesNotExist:
            MonthlySum.objects.create(
                billingCycle=billingCycle, businessLine=business_line, env=env,
                pretaxAmount=item.get('sum'), productName=item.get('productName')

            )
        else:
            MonthlySum.objects.filter(businessLine=business_line, env=env, billingCycle=billingCycle,
                                    productName=item.get('productName')).update(
                billingCycle=billingCycle, businessLine=business_line, env=env,
                pretaxAmount=item.get('sum'), productName=item.get('productName')

            )

    return True

if __name__ == '__main__':
    print ("sync start -----------------------------------")
    import time
    print (time.asctime( time.localtime(time.time()) ))

    bus_env = MonthlybillInfo.objects.values('businessLine', 'env', 'billingCycle').distinct()
    for i in bus_env:
        get_monthly_sum(i.get('businessLine'), i.get('env'), i.get('billingCycle'))
        print ('='*20)

    print ("sync completed -------------------------------")
    print (time.asctime( time.localtime(time.time()) ))