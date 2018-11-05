# -*- coding: utf8 -*-
'''
获取弹性公网IP的相关信息存储到数据库
'''
import os
import sys
import json
import math
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeEipAddressesRequest

# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from api.models import EipInfo, EcsInfo, SlbInfo, KeyIdSecret
from utils.ecs.utils import get_nat
from django.conf import settings

def get_key():
    '''获取key'''

    objs = KeyIdSecret.objects.all()
    result = []
    for i in objs:
        obj = KeyIdSecret.objects.filter(keyId=i).values('keyId', 'keySecret', 'regionId').first()
        key_id = obj['keyId']
        key_secret = obj['keySecret']
        region_ids = obj['regionId'].split(',')
        for region_id in region_ids:
            result.append({'key_id': key_id, 'key_secret': key_secret, 'region_id': region_id })

    return result

def get_eip_info(keys):

    '''
    keys字典内包含key_id key_secret region_id
    :param keys:
    :return:
    '''

    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']

    try:
        client = AcsClient(key_id, key_secret, region_id)
        request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
        request.set_PageSize(100)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        Items = response_json['EipAddresses']['EipAddress']


        for item in Items:

            allocationId = item.get('AllocationId')
            instanceId = item.get('InstanceId')
            instanceType = item.get('InstanceType')
            if instanceType == 'SlbInstance':
                allocationName = SlbInfo.objects.filter(instanceId=instanceId).values('instanceName').first().get('instanceName')
                businessLine = allocationName.split('-')[0]
                env = allocationName.split('-')[1]
            elif instanceType == 'EcsInstance':
                allocationName = EcsInfo.objects.filter(instanceId=instanceId).values('instanceName').first().get('instanceName')
                businessLine = allocationName.split('-')[0]
                env = allocationName.split('-')[1]
            elif instanceType == 'Nat':
                keys['instanceId'] = instanceId
                allocationName = get_nat(keys).get('Name')
                businessLine = allocationName.split('-')[0]
                env = allocationName.split('-')[1]
            else:
                allocationName = ''
                businessLine = ''
                env = ''
            productCode = 'eip'
            regionId = item.get('RegionId')
            status = item.get('Status')
            ipaddress = item.get('IpAddress')
            creationTime = item.get('AllocationTime')
            expiredTime = item.get('ExpiredTime')

            # print (
            #     allocationId,allocationName,instanceId,instanceType,status, businessLine, env,
            #     productCode,regionId,ipAddress,creationTime,expiredTime
            # )

            try:
                EipInfo.objects.get(allocationId = allocationId)
            except EipInfo.DoesNotExist:
                EipInfo.objects.create(
                    allocationId = allocationId, allocationName = allocationName, instanceId = instanceId,
                    instanceType = instanceType, businessLine = businessLine, env = env, status = status,
                    productCode = productCode,regionId = regionId, ipaddress = ipaddress,
                    creationTime = creationTime, expiredTime = expiredTime
                )
            else:
                EipInfo.objects.filter(allocationId = allocationId).update(
                    allocationId=allocationId, allocationName=allocationName, instanceId=instanceId,
                    instanceType=instanceType, businessLine=businessLine, env=env, status=status,
                    productCode=productCode, regionId=regionId, ipaddress=ipaddress,
                    creationTime=creationTime, expiredTime=expiredTime
                )

    except Exception as e:
        print (e)


if __name__ == '__main__':
    print ("sync start -----------------------------------")
    import time
    print (time.asctime( time.localtime(time.time()) ))

    for keys in get_key():
        get_eip_info(keys)

    print ("sync completed -------------------------------")
    print (time.asctime( time.localtime(time.time()) ))