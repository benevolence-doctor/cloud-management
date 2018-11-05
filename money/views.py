# -*- coding: utf8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from utils.money.utils import monthlybill, monthlyinstanceconsumption, accountbalance, availableinstances
from api import models

class MonthlyBillView(APIView):
    '''
    月账单查询
    '''

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            key_id = request._request.POST.get('key_id')
            key_secret = request._request.POST.get('key_secret')
            month = request._request.POST.get('month')
            result = monthlybill(key_id, key_secret, month)
            if result:
                ret['data'] = result
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return JsonResponse(ret)

class ModelMonthlySumSerializer(serializers.ModelSerializer):
    billingCycle = serializers.CharField(max_length=255)
    productName = serializers.CharField(max_length=255)
    businessLine = serializers.CharField(max_length=255)
    env = serializers.CharField(max_length=255)
    pretaxAmount = serializers.FloatField()

    class Meta:
        model = models.MonthlySum
        fields = ['billingCycle', 'productName', 'businessLine', 'env', 'pretaxAmount']


class MonthlySumView(APIView):
    '''
    产品code业务线和环境月账单汇总查询
    '''

    def get(self, request, *args, **kwargs):

        # 序列化，将数据库查询字段序列化为字典
        data_list = models.MonthlySum.objects.all()
        ser = ModelMonthlySumSerializer(instance=data_list, many=True)

        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        ser = ModelMonthlySumSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)

        return Response('POST请求，响应内容')

class AccountBalanceView(APIView):
    '''
    查询可用余额信息
    '''

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            key_id = request._request.POST.get('key_id')
            key_secret = request._request.POST.get('key_secret')
            result = accountbalance(key_id, key_secret)
            if result:
                ret['data'] = result
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return JsonResponse(ret)

class AvailableInstancesView(APIView):
    '''
    实例查询接口，查询用户可用实例列表
    '''

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            key_id = request._request.POST.get('key_id')
            key_secret = request._request.POST.get('key_secret')
            pagenum = request._request.POST.get('pagenum')
            result = availableinstances(key_id, key_secret, pagenum)
            result_total = []
            if result:
                for pagenums in range(2, int(result[0]['TotalNum']) + 1):
                    results = availableinstances(key_id, key_secret, month, pagenum)
                    results.pop(0)
                    result_total.extend(results)
            result_total.extend(result)
            ret['data'] = {'TotalCount': result[0]['TotalCount'],
                           'Instancelist': result[1:]}
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return JsonResponse(ret)

