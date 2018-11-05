# -*- coding: utf8 -*-
'''
获取实例账单详情的相关信息存储到数据库
'''
import os
import sys
import json
import math
from aliyunsdkcore.client import AcsClient
from aliyunsdkbssopenapi.request.v20171214 import QueryMonthlyInstanceConsumptionRequest

# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from api.models import EcsInfo, EipInfo, RdsInfo, SlbInfo, MonthlybillInfo, ProductName, KeyIdSecret
from utils.ecs.utils import  get_yundisk_info, get_nat
from django.conf import settings

def get_key_bss():
    '''获取key'''

    objs = KeyIdSecret.objects.all()
    result = []
    for i in objs:
        obj = KeyIdSecret.objects.filter(keyId=i).values('keyId', 'keySecret', 'regionId', 'defaultEnv').first()
        key_id = obj['keyId']
        key_secret = obj['keySecret']
        regionId = obj['regionId']
        default_env = obj['defaultEnv']
        result.append({'key_id': key_id, 'key_secret': key_secret, 'region_id': regionId, 'default_env': default_env})

    return result

def get_monthlybill_info(keys, month):
    '''
    实例月账单详情查询
    :param keys:
    :param month: 查询月份 格式为 2018-09
    :return:
    '''

    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']
    default_env = keys['default_env']
    try:
        client = AcsClient(key_id, key_secret)
        request = QueryMonthlyInstanceConsumptionRequest.QueryMonthlyInstanceConsumptionRequest()
        request.set_BillingCycle(month)
        request.set_endpoint('business.aliyuncs.com')
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        TotalCount = response_json['Data']['TotalCount']
        PageSize = response_json['Data']['PageSize']
        PageNum = response_json['Data']['PageNum']
        TotalNum = math.ceil(int(TotalCount)/int(PageSize))
        result = [{'TotalCount': TotalCount, 'TotalNum': TotalNum, 'PageNum': PageNum}]

        for pagenums in range(1, int(result[0]['TotalNum']) + 1):
            request = QueryMonthlyInstanceConsumptionRequest.QueryMonthlyInstanceConsumptionRequest()
            request.set_BillingCycle(month)
            request.set_endpoint('business.aliyuncs.com')
            request.set_PageNum(pagenums)
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            Items = response_json['Data']['Items']['Item']

            for item in Items:
                subscriptionType = item.get('SubscriptionType')
                pretaxAmount = item.get('PretaxAmount')
                productCode = item.get('ProductCode')
                regionId = item.get('Region', '')
                productName = ProductName.objects.filter(productcode=productCode).first()
                instanceId = item['InstanceID'].split(';')[0]

                if productCode == 'ecs':
                    instanceName = EcsInfo.objects.filter(instanceId=instanceId).values('instanceName').first().get('instanceName')
                elif productCode == 'rds':
                    instanceName = RdsInfo.objects.filter(instanceId=instanceId).values('instanceName').first().get('instanceName')
                elif productCode == 'slb':
                    instanceName = SlbInfo.objects.filter(instanceId=instanceId).values('instanceName').first().get('instanceName')
                elif productCode == 'eip':
                    instanceName = EipInfo.objects.filter(allocationId=instanceId).values('allocationName').first().get('allocationName')
                elif productCode == 'yundisk':
                    keys['instanceId'] = instanceId
                    instanceIds = get_yundisk_info(keys).get('instanceId')
                    instanceName = EcsInfo.objects.filter(instanceId=instanceIds).values('instanceName').first().get('instanceName')
                elif productCode == 'nat_gw':
                    keys['instanceId'] = instanceId
                    instanceName = get_nat(keys).get('Name')
                else:
                    instanceName = ''

                if instanceName:
                    businessLine = instanceName.split('-')[0]
                    env = instanceName.split('-')[1]
                else:
                    businessLine = default_env.split('-')[0]
                    env = default_env.split('-')[1]

                try:
                    MonthlybillInfo.objects.get(instanceId = instanceId)
                except MonthlybillInfo.DoesNotExist:
                    MonthlybillInfo.objects.create(
                        subscriptionType = subscriptionType, pretaxAmount = pretaxAmount, productCode = productCode,
                        productName = productName, instanceId = instanceId, instanceName = instanceName,
                        businessLine = businessLine, env = env, billingCycle = month, regionId = regionId
                    )
                else:
                    MonthlybillInfo.objects.filter(instanceId = instanceId).update(
                        subscriptionType = subscriptionType, pretaxAmount = pretaxAmount, productCode = productCode,
                        instanceName = instanceName, regionId = regionId,businessLine = businessLine, env = env
                    )


    except Exception as e:
        print (e)

    return True


if __name__ == '__main__':
    print ("sync start -----------------------------------")
    import time
    print (time.asctime( time.localtime(time.time()) ))
    month = '2018-09'
    for keys in get_key_bss():
        get_monthlybill_info(keys, month)

    print ("sync completed -------------------------------")
    print (time.asctime( time.localtime(time.time()) ))