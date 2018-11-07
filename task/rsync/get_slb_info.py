# -*- coding: utf8 -*-
'''
获取负载均衡SLB实例的相关信息存储到数据库
'''
import os
import sys
import json
import math
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest, DescribeLoadBalancerAttributeRequest


# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from api.models import EipInfo, EcsInfo, SlbInfo, KeyIdSecret
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

def get_slb_info(keys):
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
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_PageSize(100)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        Items = response_json['LoadBalancers']['LoadBalancer']


        for item in Items:
            instanceId = item.get('LoadBalancerId')
            instanceName = item.get('LoadBalancerName')
            productCode = 'slb'
            businessLine = instanceName.split('-')[0]
            env = instanceName.split('-')[0]
            regionId = item.get('RegionId')
            instanceNetworkType = item.get('NetworkType')
            internetChargeType = item.get('InternetChargeType')
            ipaddress = item.get('Address')
            keys['instanceId'] = instanceId
            ListenPorts = get_slb_item(keys).get('ListenPorts')
            creationTime = item.get('CreateTime')
            expiredTime = get_slb_item(keys).get('expiredTime')

            status = item.get('LoadBalancerStatus')
            if status == 'active':
                status = '运行中'
            elif status == 'inactive':
                status = '停止'

            BackendServer_re = get_slb_item(keys).get('BackendServers')
            BackendServers = []
            for i in BackendServer_re:
                i_re = EcsInfo.objects.filter(instanceId=i).values('instanceName').first()
                if i_re is not None:
                    BackendServers.append(i_re.get('instanceName'))
                else:
                    BackendServers.append(i)

            # print(
            #     instanceId, instanceName, productCode, businessLine, env, regionId, status,
            #     instanceNetworkType, ipaddress, BackendServers, ListenPorts, creationTime, expiredTime
            # )
            try:
                SlbInfo.objects.get(instanceId = instanceId)
            except SlbInfo.DoesNotExist:
                SlbInfo.objects.create(
                    instanceId = instanceId, instanceName = instanceName, productCode = productCode, env = env,
                    businessLine = businessLine, regionId = regionId, status = status, ipaddress = ipaddress,
                    instanceNetworkType = instanceNetworkType, internetChargeType = internetChargeType,
                    BackendServers = BackendServers,ListenPorts = ListenPorts,
                    creationTime = creationTime, expiredTime = expiredTime
                )
            else:
                SlbInfo.objects.filter(instanceId = instanceId).update(
                    instanceId=instanceId, instanceName=instanceName, productCode=productCode, env=env,
                    businessLine=businessLine, regionId=regionId, status=status, ipaddress=ipaddress,
                    instanceNetworkType=instanceNetworkType, internetChargeType = internetChargeType,
                    BackendServers=BackendServers,ListenPorts=ListenPorts,
                    creationTime=creationTime, expiredTime=expiredTime
                )

    except Exception as e:
        print (e)


def get_slb_item(keys):
    '''
    获取单个slb信息
    :param keys:
    :return:
    '''
    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']
    instanceId = keys['instanceId']
    result = {}

    try:
        client = AcsClient(key_id, key_secret, region_id)
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(instanceId)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        BackendServers = [i.get('ServerId') for i in response_json.get('BackendServers').get('BackendServer')]
        ListenPorts = [i.get('ListenerProtocal') + ':' + str(i.get('ListenerPort')) for i in
                       response_json.get('ListenerPortsAndProtocal').get('ListenerPortAndProtocal')]
        expiredTime = response_json.get('EndTime')
        result['BackendServers'] = BackendServers
        result['ListenPorts'] = ListenPorts
        result['expiredTime'] = expiredTime

    except Exception as e:
        print (e)

    return  result

if __name__ == '__main__':
    print ("sync start -----------------------------------")
    import time
    print (time.asctime( time.localtime(time.time()) ))

    for keys in get_key():
        get_slb_info(keys)

    print ("sync completed -------------------------------")
    print (time.asctime( time.localtime(time.time()) ))