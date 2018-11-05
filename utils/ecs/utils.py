# -*- coding: utf8 -*-
"""
查询ECS实例的信息
InstanceChargeType 付费方式
PrePaid：预付费（包年包月 ）
PostPaid：按量付费
"""

import json
import math
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeDisksRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest, DescribeNatGatewaysRequest


def get_ecs_ids(keys):
    '''
    获取所有ECS的实例id
    :return:
    '''

    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']
    client = AcsClient(key_id, key_secret, region_id)
    try:
        request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        TotalCount = response_json['TotalCount']
        PageSize = response_json['PageSize']
        PageNum = response_json['PageNumber']
        TotalNum = math.ceil(int(TotalCount) / int(PageSize))
        result = [{'TotalCount': TotalCount, 'TotalNum': TotalNum, 'PageNum': PageNum}]
        for pagenums in range(1, int(result[0]['TotalNum']) + 1):
            request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
            request.set_PageNumber(pagenums)
            response = client.do_action_with_exception(request)
            response_json = json.loads(response)
            Items = response_json['InstanceStatuses']['InstanceStatus']
            for item in Items:
                result.append(item['InstanceId'])

    except Exception as e:
        print(e)
        result = []

    return result

def get_ecs_info(keys):
    '''
    通过实例ID获取单个或多个实例详情,最多支持100个实例
    :param InstanceIds: 实例ID列表
    :return:
    '''
    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']
    InstanceIds = [keys['instanceIds']]
    client = AcsClient(key_id, key_secret, region_id)
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_PageSize(100)
    request.set_InstanceIds(InstanceIds)

    try:
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        TotalCount = response_json['TotalCount']
        result = [{'TotalCount': TotalCount}]
        Items = response_json['Instances']['Instance']

        for item in Items:
            InstanceNetworkType = item['InstanceNetworkType']
            if InstanceNetworkType == 'vpc':
                PrimaryIpAddress = item['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
                PublicIpAddress = item['EipAddress']['IpAddress']
            elif InstanceNetworkType == 'classic':
                PrimaryIpAddress = item['InnerIpAddress']['IpAddress'][0]
                PublicIpAddress = item['PublicIpAddress']['IpAddress'][0]
            ZoneId = item['ZoneId']
            RegionId = item['RegionId']
            Cpu = item['Cpu']
            Memory = item['Memory']
            OSType = item['OSType']
            OSName = item['OSName']
            Status = item['Status']
            CreationTime = item['CreationTime']
            ExpiredTime = item['ExpiredTime']
            InstanceId = item['InstanceId']
            InstanceName = item['InstanceName']
            InstanceChargeType = item['InstanceChargeType']
            result.append({
                'InstanceId': InstanceId,
                'InstanceName': InstanceName,
                'InstanceChargeType': InstanceChargeType,
                'ZoneId': ZoneId,
                'RegionId': RegionId,
                'Cpu': Cpu,
                'Memory': Memory,
                'OSType': OSType,
                'OSName': OSName,
                'Status': Status,
                'CreationTime': CreationTime,
                'ExpiredTime': ExpiredTime
            })
    except Exception as e:
        print(e)
        result = []

    return result

def get_yundisk_size(keys):
    '''
    根据InstanceId获取磁盘大小
    :param keys:
    :return:
    '''
    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']
    instanceId = keys['instanceId']
    Size = []

    try:
        client = AcsClient(key_id, key_secret, region_id)
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_InstanceId(instanceId)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        for i in response_json['Disks']['Disk']:
            Size.append(i['Size'])
    except:
        Size = []

    return Size

def get_yundisk_info(keys):
    '''
    根据InstanceId获取磁盘大小
    :param keys:
    :return:
    '''
    key_id = keys['key_id']
    key_secret = keys['key_secret']
    region_id = keys['region_id']
    diskIds = [keys['instanceId']]
    result = {}

    try:
        client = AcsClient(key_id, key_secret, region_id)
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_DiskIds(diskIds)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        for item in response_json['Disks']['Disk']:
            result['diskId'] = item.get('DiskId')
            result['instanceId'] = item.get('InstanceId')
            result['size'] = item.get('Size')
            result['status'] = item.get('Status')
            result['creationTime'] = item.get('CreationTime')
            result['expiredTime'] = item.get('ExpiredTime')

    except Exception as e:
        print (e)

    return result

def get_nat(keys):
    '''
    获取nat信息
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
        request = DescribeNatGatewaysRequest.DescribeNatGatewaysRequest()
        request.set_NatGatewayId(instanceId)
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        Items = response_json['NatGateways']['NatGateway']
        for item in Items:
            result['Name'] = item.get('Name')
            result['Status'] = item.get('Status')
            result['Spec'] = item.get('Spec')

    except Exception as e:
        print (e)

    return result


# try:
#     keys = {
#         'key_id': 'LTAIEsW5u3Mdv0DY',
#         'key_secret': 'UVko4RRAT2F8Q350H1hUSdhURQHDUZ',
#         'region_id': 'cn-shanghai',
#         'instanceId': 'd-uf6bhisalou7qj2ifmnk'
#
#     }
#     print (get_yundisk_info(keys))
# except Exception as e:
#     print (e)