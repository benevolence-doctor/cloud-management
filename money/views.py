# -*- coding: utf8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.money.utils import monthlybill, accountbalance, availableinstances
from api import models
from django.db.models import Sum, Count, Q
from utils.money import utils
from utils.base import base
from utils.serializers import serializers

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

class MonthlySumView(APIView):
    '''
    产品code业务线和环境月账单汇总查询
    '''

    def post(self, request, *args, **kwargs):

        businessLine = request._request.POST.get('business_line')
        env = request._request.POST.get('env')
        billingCycle = request._request.POST.get('billing_cycle')
        result = {'code': 1000, 'msg': None}
        bus_re = models.MonthlySum.objects.filter(billingCycle=billingCycle).values('businessLine').distinct()
        bus_list = [i.get('businessLine') for i in bus_re]
        env_re = models.MonthlySum.objects.filter(billingCycle=billingCycle).values('env').distinct()
        env_list = [i.get('env') for i in env_re]

        try:
            if businessLine =='all'  and env == 'all':
                keys = {'billingCycle': billingCycle, 'businessLine': bus_list, 'env': env_list}
            elif businessLine == 'all' and env != 'all':
                keys = {'billingCycle': billingCycle, 'businessLine': bus_list, 'env': env.split(',')}
            elif businessLine != 'all' and env == 'all':
                keys = {'billingCycle': billingCycle, 'businessLine': businessLine.split(','), 'env': env_list}
            else:
                keys = {'billingCycle': billingCycle, 'businessLine': businessLine.split(','), 'env': env.split(',')}

            bs_env = utils.get_business_env_money(keys)
            sum_money = sum([i.get('sum_money') for i in bs_env])
            sum_num = sum([i.get('sum_num') for i in bs_env])
            totals = {'sum_money': sum_money,'sum_num': sum_num }
            result['totals'] = totals
            result['data'] = bs_env

        except Exception as e:
            result['code'] = 1002
            result['msg'] = str(e)

        return Response(result)

class AccountBalanceView(APIView):
    '''
    查询可用余额信息
    '''

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        result = []
        try:
            key_list = base.get_key().get('data')
            for keys in key_list:
                ac_result = accountbalance(keys)
                result.append(ac_result)
            if result:
                ret['data'] = result
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return JsonResponse(ret)

class MonthlybillInfoView(APIView):

    def post(self, request, *args, **kwargs):

        businessLine = request._request.POST.get('business_line')
        env = request._request.POST.get('env')
        billingCycle = request._request.POST.get('billing_cycle')
        ret = {'code': 1000, 'msg': None}

        try:

            if businessLine =='all'  and env == 'all':
                data_list = models.MonthlybillInfo.objects.filter(billingCycle=billingCycle)
                keys = {'billingCycle': billingCycle}
            elif businessLine == 'all' and env != 'all':
                data_list = models.MonthlybillInfo.objects.filter(env=env, billingCycle=billingCycle)
                keys = {'billingCycle': billingCycle, 'env': env}
            elif businessLine != 'all' and env == 'all':
                data_list = models.MonthlybillInfo.objects.filter(businessLine=businessLine, billingCycle=billingCycle)
                keys = {'billingCycle': billingCycle, 'businessLine': businessLine}
            else:
                data_list = models.MonthlybillInfo.objects.filter(businessLine=businessLine, env=env, billingCycle=billingCycle)
                keys = {'billingCycle': billingCycle, 'businessLine': businessLine, 'env': env}

            ser = serializers.MonthlybillInfoSerializer(instance=data_list, many=True)

            ret['totals'] = utils.get_productcode_num(str(keys))
            ret['data'] = ser.data

        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return Response(ret)

class EcsInfoView(APIView):
    '''ECS实例'''

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            data_list = models.EcsInfo.objects.all()
            ser = serializers.EcsInfoSerializer(instance=data_list, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return Response(ret)

class EcsInfoIdView(APIView):

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:

            data_list = models.EcsInfo.objects.filter(pk=id).first()
            ser = serializers.EcsInfoSerializer(instance=data_list)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return Response(ret)

class RdsInfoView(APIView):
    '''RDS实例'''

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            data_list = models.RdsInfo.objects.all()
            ser = serializers.RdsInfoSerializer(instance=data_list, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return Response(ret)

class SlbInfoView(APIView):
    '''负载均衡SLB实例'''

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            data_list = models.SlbInfo.objects.all()
            ser = serializers.SlbInfoSerializer(instance=data_list, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return Response(ret)

class EipInfoView(APIView):
    '''弹性公网IP实例'''

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            data_list = models.EipInfo.objects.all()
            ser = serializers.EipInfoSerializer(instance=data_list, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return Response(ret)
