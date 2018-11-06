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

def get_test(keys):
    billingCycle = keys.get('billingCycle', '')
    businessLine = keys.get('businessLine', '')
    env = keys.get('env', '')
    if businessLine == '' and env == '':
        filters = (Q(billingCycle=billingCycle))
    elif businessLine == '' and env != '':
        filters = (Q(billingCycle=billingCycle) & Q(env=env))
    elif businessLine != '' and env == '':
        filters = (Q(billingCycle=billingCycle) & Q(businessLine=businessLine))
    elif businessLine != '' and env != '':
        filters = (Q(billingCycle=billingCycle) & Q(businessLine=businessLine) & Q(env=env))

    print (filters)
    obj = MonthlybillInfo.objects.filter(filters).values('productCode').distinct()

    result = {}
    for i in obj:
        productCode = i.get('productCode')
        cobj = MonthlybillInfo.objects.filter(filters,productCode=productCode ).values(
            'productCode').annotate(count=Count('productCode')).values('productCode' ,'count')[0]
        result['billingCycle'] = billingCycle
        result[cobj.get('productCode')] = cobj.get('count')
    print (result)

def get_hh(keys):
    return  keys
try:
    keys = {
        'billingCycle': '2018-09',
        'businessLine': 'ding',
        'env': 'uat'
    }
    b = get_hh(keys)
    print (b)
    c = base.get_produc(str(keys))
    print (c)
except Exception as e:
    print (e)