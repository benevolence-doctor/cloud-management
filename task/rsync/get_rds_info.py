# -*- coding: utf8 -*-
'''
获取RDS实例的相关信息存储到数据库
'''
import os
import sys
import json
import math
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceNetInfoRequest

# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from api.models import RdsInfo, KeyIdSecret
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

def get_rds_info(keys):
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
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_PageSize(100)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        Items = response_json['Items']['DBInstance']

        for item in Items:
            instanceId = item.get('DBInstanceId')
            instanceName = item.get('DBInstanceDescription')
            productCode = 'rds'
            businessLine = instanceName.split('-')[0]
            env = instanceName.split('-')[1]
            regionId = item.get('RegionId')
            status = item.get('DBInstanceStatus')
            instanceNetworkType = item.get('InstanceNetworkType')
            keys['DBInstanceId'] = instanceId
            rds_item = get_rds_item(keys)
            rds_network = get_rds_network(keys)
            publicIpAddress = rds_network.get('publicIpAddress', '')
            primaryIpAddress = rds_network.get('primaryIpAddress', '')
            cpuMemory = rds_item.get('cpuMemory')
            engine = item.get('Engine') + " " + item.get('EngineVersion')
            instanceType = item.get('DBInstanceType')
            masterInstanceId = rds_item.get('masterInstanceId')
            guardDBInstanceId = rds_item.get('guardDBInstanceId')
            readOnlyDBInstanceId = rds_item.get('readOnlyDBInstanceId')
            creationTime = item.get('CreateTime')
            expiredTime = item.get('ExpireTime')

            try:
                RdsInfo.objects.get(instanceId = instanceId)
            except RdsInfo.DoesNotExist:
                RdsInfo.objects.create(
                    instanceId = instanceId, instanceName = instanceName, productCode = productCode,
                    businessLine = businessLine, env = env, regionId = regionId, status = status,
                    instanceNetworkType = instanceNetworkType, publicIpAddress = publicIpAddress,
                    primaryIpAddress = primaryIpAddress, cpuMemory = cpuMemory, engine = engine,
                    instanceType = instanceType, masterInstanceId = masterInstanceId,
                    guardDBInstanceId = guardDBInstanceId, readOnlyDBInstanceId = readOnlyDBInstanceId,
                    creationTime = creationTime, expiredTime = expiredTime
                )
            else:
                RdsInfo.objects.filter(instanceId = instanceId).update(
                    instanceId=instanceId, instanceName=instanceName, productCode=productCode,
                    businessLine=businessLine, env=env, regionId=regionId, status=status,
                    instanceNetworkType=instanceNetworkType, publicIpAddress=publicIpAddress,
                    primaryIpAddress=primaryIpAddress, cpuMemory=cpuMemory, engine=engine,
                    instanceType=instanceType, masterInstanceId=masterInstanceId,
                    guardDBInstanceId=guardDBInstanceId, readOnlyDBInstanceId=readOnlyDBInstanceId,
                    creationTime=creationTime, expiredTime=expiredTime
                )

    except Exception as e:
        print (e)

    return  True

def get_rds_item(keys):
    '''
    通过实例ID获取该实例详情
    :param keys:
    :return:
    '''
    key_id = keys['key_id']
    key_secret = keys['key_secret']
    DBInstanceId = keys['DBInstanceId']
    result = {}
    try:
        client = AcsClient(key_id, key_secret)
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(DBInstanceId)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        Items = response_json['Items']['DBInstanceAttribute'][0]
        Cpu = str(Items['DBInstanceCPU'])
        Memory = str(math.floor(Items['DBInstanceMemory']/1024))
        result['cpuMemory'] = Cpu + 'CPU' + ' ' + Memory+ 'GB'

        if Items.get('masterInstanceId') == None:
            result['masterInstanceId'] = ''
        else:
            result['masterInstanceId'] = Items.get('masterInstanceId')
        if Items.get('guardDBInstanceId') == None:
            result['guardDBInstanceId'] = ''
        else:
            result['guardDBInstanceId'] = Items.get('guardDBInstanceId')
        if not Items.get('ReadOnlyDBInstanceIds').get('ReadOnlyDBInstanceId'):
            result['readOnlyDBInstanceId'] = ''
        else:
            result['readOnlyDBInstanceId'] = [i.get('DBInstanceId') for i in Items.get('ReadOnlyDBInstanceIds').get('ReadOnlyDBInstanceId')]

    except Exception as e:
        print (e)

    return  result

def get_rds_network(keys):
    '''获取RDS实例的内外网地址'''
    key_id = keys['key_id']
    key_secret = keys['key_secret']
    DBInstanceId = keys['DBInstanceId']
    result = {}

    try:
        client = AcsClient(key_id, key_secret)
        request = DescribeDBInstanceNetInfoRequest.DescribeDBInstanceNetInfoRequest()
        request.set_DBInstanceId(DBInstanceId)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        Items = response_json['DBInstanceNetInfos']['DBInstanceNetInfo']

        for item in Items:
            if item['IPType'] == 'Private':
                result['primaryIpAddress'] = item.get('ConnectionString')
            elif item['IPType'] == 'Public':
                result['publicIpAddress'] = item.get('ConnectionString')

    except Exception as e:
        print (e)

    return  result

if __name__ == '__main__':
    print ("sync start -----------------------------------")
    import time
    print (time.asctime( time.localtime(time.time()) ))

    for keys in get_key():
        get_rds_info(keys)

    print ("sync completed -------------------------------")
    print (time.asctime( time.localtime(time.time()) ))