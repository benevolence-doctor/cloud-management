# -*- coding: utf8 -*-
'''
获取ECS的相关信息存储到数据库
'''
import os
import sys
import json
import math
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest

# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from api.models import EcsInfo, KeyIdSecret
from utils.ecs.utils import  get_yundisk_size
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

def get_ecs_info(keys):
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
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        TotalCount = response_json['TotalCount']
        PageSize = response_json['PageSize']
        PageNum = response_json['PageNumber']
        TotalNum = math.ceil(int(TotalCount) / int(PageSize))
        result = [{'TotalCount': TotalCount, 'TotalNum': TotalNum, 'PageNum': PageNum}]

        for pagenums in range(1, int(result[0]['TotalNum']) + 1):
            request = DescribeInstancesRequest.DescribeInstancesRequest()
            request.set_PageNumber(pagenums)
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            Items = response_json['Instances']['Instance']

            for item in Items:
                instanceNetworkType = item['InstanceNetworkType']
                if instanceNetworkType == 'vpc':
                    primaryIpAddress = item['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
                    publicIpAddress = item['EipAddress']['IpAddress']
                elif instanceNetworkType == 'classic':
                    primaryIpAddress = item['InnerIpAddress']['IpAddress'][0]
                    publicIpAddress = item['PublicIpAddress']['IpAddress'][0]

                instanceId = item['InstanceId']
                instanceName = item['InstanceName']
                productCode = 'ecs'
                businessLine = instanceName.split('-')[0]
                env = instanceName.split('-')[1]
                regionId = item['RegionId']
                status = item['Status']
                cpu = item['Cpu']
                memory = item['Memory']/1024
                cpuMemory = str(cpu) + 'vCpu' + ' ' + str(memory) + 'G'
                keys['instanceId'] = instanceId
                yunDisk = get_yundisk_size(keys)
                osType = item['OSType']
                osName = item['OSName']
                hostname = item['HostName']
                creationTime = item['CreationTime']
                expiredTime = item['ExpiredTime']

                try:
                    EcsInfo.objects.get(instanceId = instanceId)
                except EcsInfo.DoesNotExist:
                    EcsInfo.objects.create(
                        instanceId = instanceId, instanceName = instanceName, productCode= productCode,
                        businessLine = businessLine,env =env, regionId = regionId, hostname = hostname,
                        cpuMemory = cpuMemory,instanceNetworkType = instanceNetworkType,
                        publicIpAddress = publicIpAddress,primaryIpAddress = primaryIpAddress,
                        yunDisk = yunDisk, osType = osType, osName = osName,status = status,
                        creationTime = creationTime, expiredTime = expiredTime
                    )
                else:
                    EcsInfo.objects.filter(instanceId = instanceId).update(
                        instanceId = instanceId, instanceName = instanceName, productCode = productCode,
                        businessLine = businessLine, env = env, regionId = regionId, hostname = hostname,
                        cpuMemory=cpuMemory, instanceNetworkType = instanceNetworkType,
                        publicIpAddress = publicIpAddress, primaryIpAddress = primaryIpAddress,
                        yunDisk = yunDisk, osType=osType, osName = osName, status = status,
                        creationTime=creationTime, expiredTime = expiredTime
                    )

    except Exception as e:
        print(e)

    return True


if __name__ == '__main__':
    print ("sync start -----------------------------------")
    import time
    print (time.asctime( time.localtime(time.time()) ))

    for keys in get_key():
        get_ecs_info(keys)

    print ("sync completed -------------------------------")
    print (time.asctime( time.localtime(time.time()) ))