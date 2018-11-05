# -*- coding: utf8 -*-
import bs4
import requests
from api.models import  BusinessLine



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

