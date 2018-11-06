# -*- coding: utf8 -*-
import sys
import os
import bs4
import requests


# # 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()


from api.models import  BusinessLine, KeyIdSecret
from rest_framework import serializers
from django.conf import settings



def get_productname(productcode):
    '''
    通过产品code获取商品name
    :param ProductCode: 产品code
    :return: 商品nam

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


class KeyIdSecretSerializer(serializers.ModelSerializer):
    keyId = serializers.CharField(max_length=255)
    keySecret = serializers.CharField(max_length=255)
    regionId = serializers.CharField(max_length=255)
    accountNumber = serializers.CharField(max_length=255)
    defaultEnv = serializers.CharField(max_length=255)
    remark = serializers.CharField(max_length=255)

    class Meta:
        model = KeyIdSecret
        fields = '__all__'



def get_key():
    '''获取key'''
    result = {}
    data_list = KeyIdSecret.objects.all()
    ser = KeyIdSecretSerializer(instance=data_list, many=True)
    result['data'] = ser.data

    return result
