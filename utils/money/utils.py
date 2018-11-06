# -*- coding: utf8 -*-
import math
import json
from utils.base.base import get_productname
from aliyunsdkcore.client import AcsClient
from aliyunsdkbssopenapi.request.v20171214 import QueryMonthlyBillRequest
from aliyunsdkbssopenapi.request.v20171214 import QueryAccountBalanceRequest
from aliyunsdkbssopenapi.request.v20171214 import QueryAvailableInstancesRequest
from django.db.models import Sum, Count, Q
from api.models import KeyIdSecret, MonthlybillInfo, MonthlySum

def monthlybill(id, month):
    '''
    月账单查询
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :param month: 查询月份 格式为 2018-09
    :return: 返回一个列表
    '''

    obj = BusinessLine.objects.filter(pk=id).values('key_id', 'key_secret').first()
    key_id = obj['key_id']
    key_secret = obj['key_secret']
    client = AcsClient(key_id, key_secret);
    request = QueryMonthlyBillRequest.QueryMonthlyBillRequest()
    request.set_BillingCycle(month)
    request.set_endpoint("business.aliyuncs.com")
    result = []

    try:
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        for item in response_json['Data']['Items']['Item']:
            SubscriptionType = item['SubscriptionType']
            PaymentAmount = item['PaymentAmount']
            ProductCode = item['ProductCode']

            if SubscriptionType == 'PayAsYouGo':
                SubscriptionType = '后付费'
            elif SubscriptionType == 'Subscription':
                SubscriptionType = '预付费'

            result.append({'产品名称': ProductCode,
                      '付费方式': SubscriptionType,
                      '付费金额': PaymentAmount
                      })
    except Exception as e:
        print (e)

    return result

def accountbalance(keys):
    '''
    查询账户余额信息
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :return: 返回一个字典
    '''

    key_id = keys.get('keyId')
    key_secret = keys.get('keySecret')
    remark = keys.get('remark')
    accountNumber = keys.get('accountNumber')

    client = AcsClient(key_id, key_secret);
    request = QueryAccountBalanceRequest.QueryAccountBalanceRequest()
    request.set_endpoint("business.aliyuncs.com")
    result = {}
    try:
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        result['阿里云账号'] = accountNumber
        result['备注'] = remark
        result['可用余额'] = response_json['Data']['AvailableCashAmount']

    except Exception as e:
        print(e)

    return result

def availableinstances(id, pagenum):
    '''
    实例查询接口，查询用户可用实例列表
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :param pagenum: 默认为第一页 即 1
    :return: 返回一个列表
    '''

    obj = BusinessLine.objects.filter(pk=id).values('key_id', 'key_secret').first()
    key_id = obj['key_id']
    key_secret = obj['key_secret']

    client = AcsClient(key_id, key_secret, pagenum);
    request = QueryAvailableInstancesRequest.QueryAvailableInstancesRequest()
    request.set_endpoint("business.aliyuncs.com")
    request.set_PageNum(pagenum)
    request.set_PageSize(100)
    try:
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        TotalCount = response_json['Data']['TotalCount']
        PageSize = response_json['Data']['PageSize']
        PageNum = response_json['Data']['PageNum']
        TotalNum = math.ceil(int(TotalCount)/int(PageSize))
        result = [{'TotalCount': TotalCount, 'TotalNum': TotalNum, 'PageNum': PageNum}]
        Items = response_json['Data']['InstanceList']
        for item in Items:
            ProductCode = item['ProductCode']
            ProductName = get_productname(ProductCode)
            InstanceID = item['InstanceID']
            RenewStatus = item['RenewStatus']
            CreateTime = item['CreateTime']
            EndTime = item['EndTime']
            SubscriptionType = item['SubscriptionType']


            if SubscriptionType == 'PayAsYouGo':
                SubscriptionType = '后付费'
            elif SubscriptionType == 'Subscription':
                SubscriptionType = '预付费'

            if RenewStatus == 'AutoRenewal':
                RenewStatus = '自动续费'
            elif RenewStatus == 'ManualRenewal':
                RenewStatus = '手动续费'
            elif RenewStatus == 'NotRenewal':
                RenewStatus = '不续费'

            result.append({'产品名称': ProductName,
                           '实例ID': InstanceID,
                           '付费方式': SubscriptionType,
                           '续费状态': RenewStatus,
                           '创建时间': CreateTime,
                           '过期时间': EndTime
                           })

    except Exception as e:
        print(e)
        result = []

    return result

def get_productcode_num(keys):
    '''

    :param keys: billingCycle env businessLine
    :return:
    '''
    keys = eval(keys)
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


    obj = MonthlybillInfo.objects.filter(filters).values('productCode').distinct()
    result = {}

    for i in obj:
        productCode = i.get('productCode')
        cobj = MonthlybillInfo.objects.filter(filters,productCode=productCode ).values(
            'productCode').annotate(count=Count('productCode')).values('productName' ,'count')[0]
        result['billingCycle'] = billingCycle
        result[cobj.get('productName')] = cobj.get('count')

    return  result