# -*- coding: utf8 -*-
import os
import sys
import bs4
import requests

# 调试环境使用
sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()

from api.models import ProductName
from django.conf import settings

def get_productname():
    '''
    抓取阿里云页面将产品code name存入数据库
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

    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.content.decode("utf-8"), features="html.parser")
    results = []
    result = []
    productcode_list = []
    for archive in soup.select("div.markdown-body tr"):
        archive = archive.select('td')
        results.append(archive)

    for archive_list in results:
        if archive_list:
            CommodityName = archive_list[0].string
            ProductCode = archive_list[1].string
            CommodityCode = archive_list[2].string
            productcode_list.append(ProductCode)
            if ProductCode in base_productcode.keys():
                CommodityName = base_productcode[ProductCode]

            try:
                ProductName.objects.get(productcode=ProductCode)
            except ProductName.DoesNotExist:
                ProductName.objects.create(productcode=ProductCode,
                                           commodityname=CommodityName,
                                           commoditycode=CommodityCode)
            else:
                ProductName.objects.filter(productcode=ProductCode).update(
                                            productcode=ProductCode,
                                            commodityname=CommodityName,
                                            commoditycode=CommodityCode
                )

    return True

if __name__ == "__main__":
    get_productname()