# -*- coding: utf8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from utils.money.utils import monthlybill, accountbalance, availableinstances
from api import models
from django.db.models import Sum, Count



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
    instanceTotals = serializers.IntegerField()

    class Meta:
        model = models.MonthlySum
        fields = ['billingCycle', 'productName', 'businessLine', 'env', 'pretaxAmount', 'instanceTotals']


class MonthlySumView(APIView):
    '''
    产品code业务线和环境月账单汇总查询
    '''

    def get(self, request, *args, **kwargs):

        # 序列化，将数据库查询字段序列化为字典

        result = {'code': 1000, 'msg': None}
        try:
            data_list = models.MonthlySum.objects.all()
            ser = ModelMonthlySumSerializer(instance=data_list, many=True)
            result['data'] = ser.data
        except Exception as e:
            result['code'] = 1002
            result['msg'] = str(e)

        return Response(result)

    def post(self, request, *args, **kwargs):

        businessLine = request._request.POST.get('business_line')
        env = request._request.POST.get('env')
        billingCycle = request._request.POST.get('billingCycle')
        result = {'code': 1000, 'msg': None}
        try:
            if businessLine =='all'  and env == 'all':
                data_list = models.MonthlySum.objects.filter(billingCycle=billingCycle)
                totals = models.MonthlySum.objects.filter(billingCycle=billingCycle).values(
                    'billingCycle').annotate(sum_money=Sum('pretaxAmount'), sum_num=Sum('instanceTotals')
                                                                    ).values('billingCycle', 'sum_money', 'sum_num')
            elif businessLine == 'all' and env != 'all':
                data_list = models.MonthlySum.objects.filter(env=env, billingCycle=billingCycle)
                totals = models.MonthlySum.objects.filter(env=env, billingCycle=billingCycle).values(
                    'env', 'billingCycle').annotate(sum_money=Sum('pretaxAmount'), sum_num=Sum('instanceTotals')
                                                                    ).values('billingCycle', 'sum_money', 'sum_num')
            elif businessLine != 'all' and env == 'all':
                data_list = models.MonthlySum.objects.filter(businessLine=businessLine, billingCycle=billingCycle)
                totals = models.MonthlySum.objects.filter(businessLine=businessLine, billingCycle=billingCycle).values(
                    'businessLine', 'billingCycle').annotate(sum_money=Sum('pretaxAmount'), sum_num=Sum('instanceTotals')
                                                                    ).values('billingCycle', 'sum_money', 'sum_num')
            else:
                data_list = models.MonthlySum.objects.filter(businessLine=businessLine, env=env, billingCycle=billingCycle)
                totals = models.MonthlySum.objects.filter(businessLine=businessLine, env=env, billingCycle=billingCycle).values(
                    'businessLine', 'env', 'billingCycle').annotate(sum_money=Sum('pretaxAmount'), sum_num=Sum('instanceTotals')
                                                                    ).values('billingCycle', 'sum_money', 'sum_num')

            ser = ModelMonthlySumSerializer(instance=data_list, many=True)
            result['totals'] = totals
            result['data'] = ser.data

        except Exception as e:
            result['code'] = 1002
            result['msg'] = str(e)

        return Response(result)


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
