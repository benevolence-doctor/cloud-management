# -*- coding: utf8 -*-
import math
import json
import bs4
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkbssopenapi.request.v20171214 import QueryMonthlyBillRequest
from aliyunsdkbssopenapi.request.v20171214 import QueryAccountBalanceRequest
from aliyunsdkbssopenapi.request.v20171214 import QueryAvailableInstancesRequest
from aliyunsdkbssopenapi.request.v20171214 import QueryMonthlyInstanceConsumptionRequest

def md5(user):

    '''生成md5'''

    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

def get_productname(productcode):
    '''
    通过产品code获取商品name
    :param ProductCode: 产品code
    :return: 商品name
    '''

    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    url = 'https://help.aliyun.com/document_detail/92730.html'
    base_productcode = {
        'ecs': '云服务器ECS',
        'yundisk': '云盘',
        'rds': '关系型数据库RDS',
        'cdn': '内容分发网络CDN',
        'slb': '负载均衡SLB',
        'eip': '弹性公网IP',
        'ri': '高速通道',
        'oss': '对象存储OSS',
        'nat_gw': 'NAT网关',
        'nas': 'NAS文件存储',
        'vps': '专有网络VPC',
    }

    if productcode in base_productcode:
        CommodityName = base_productcode[productcode]
    else:
        response = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(response.content.decode("utf-8"), features="html.parser")
        results = []
        result = []
        productcode_list = []
        CommodityName = None
        for archive in soup.select("div.markdown-body tr"):
            archive = archive.select('td')
            results.append(archive)
            for archive_list in results:
                if archive_list:
                    CommodityName = archive_list[0].string
                    ProductCode = archive_list[1].string
                    CommodityCode = archive_list[2].string
                    productcode_list.append(ProductCode)
                    result.append({'ProductCode': ProductCode,
                                   'CommodityName': CommodityName,
                                   'CommodityCode': CommodityCode
                                   })
        if productcode in productcode_list:
            for i in result:
                if i['ProductCode'] == productcode:
                    CommodityName = i['CommodityName'].split('(')[0]

    return CommodityName

def monthlybill(key_id, key_secret, month):
    '''
    月账单查询
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :param month: 查询月份 格式为 2018-09
    :return: 返回一个列表
    '''

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

def monthlyinstanceconsumption(key_id, key_secret, month, pagenum):
    '''
    实例月账单详情查询
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :param month: 查询月份 格式为 2018-09
    :param pagenum: 默认为第一页 即 1
    :return: 返回一个列表
    '''

    client = AcsClient(key_id, key_secret);
    request = QueryMonthlyInstanceConsumptionRequest.QueryMonthlyInstanceConsumptionRequest()
    request.set_BillingCycle(month)
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
        Items =  response_json['Data']['Items']['Item']
        for item in Items:
            SubscriptionType = item['SubscriptionType']
            PretaxAmount = item['PretaxAmount']
            ProductCode = item['ProductCode']
            InstanceID = item['InstanceID']

            if SubscriptionType == 'PayAsYouGo':
                SubscriptionType = '后付费'
            elif SubscriptionType == 'Subscription':
                SubscriptionType = '预付费'

            result.append({'实例ID': InstanceID,
                           '产品名称': ProductCode,
                           '付费方式': SubscriptionType,
                           '付费金额': PretaxAmount
                           })
    except Exception as e:
        print (e)
        result = []

    return result

def accountbalance(key_id, key_secret):
    '''
    查询账户余额信息
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :return: 返回一个字典
    '''

    client = AcsClient(key_id, key_secret);
    request = QueryAccountBalanceRequest.QueryAccountBalanceRequest()
    request.set_endpoint("business.aliyuncs.com")
    result = {}
    try:
        response = client.do_action_with_exception(request)
        response_json = json.loads(response)
        result['可用余额'] = response_json['Data']['AvailableCashAmount']
        ret['data'] = result
    except Exception as e:
        print(e)

    return result

def availableinstances(key_id, key_secret, pagenum):
    '''
    实例查询接口，查询用户可用实例列表
    :param key_id: Access Key ID
    :param key_secret: Access Key Secret
    :param pagenum: 默认为第一页 即 1
    :return: 返回一个列表
    '''

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






