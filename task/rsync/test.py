# -*- coding: utf8 -*-
import os
import sys

sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()
from api.models import MonthlySum, MonthlybillInfo
from django.db.models import Sum, Count
from django.db.models import Q
from utils.base import base

keys = {
    'billingCycle': '2018-09',
    'businessLine': 'ding',
    'env': ''
}
billingCycle='2018-09'
businessLine = 'ding'
env = ''
if businessLine == '' and env == '':
    filters = (Q(billingCycle=billingCycle))
elif businessLine == '' and env != '':
    filters = (Q(billingCycle=billingCycle) & Q(env=env))
elif businessLine != '' and env == '':
    filters = (Q(billingCycle=billingCycle) & Q(businessLine=businessLine))
elif businessLine != '' and env != '':
    filters = (Q(billingCycle=billingCycle) & Q(businessLine=businessLine) & Q(env=env))


obj = MonthlybillInfo.objects.filter(filters).values('productCode').distinct()

result = {}
for i in obj:
    productCode = i.get('productCode')
    cobj = MonthlybillInfo.objects.filter(filters,productCode=productCode ).values(
        'productCode').annotate(sum_money=Sum('pretaxAmount'),count=Count('productCode')).values(
        'productCode' ,'count', 'sum_money')[0]
    result['billingCycle'] = billingCycle
    result[cobj.get('productCode')+'_count'] = cobj.get('count')
    result[cobj.get('productCode')+'_sum_money'] = cobj.get('sum_money')
print (result)