# -*- coding: utf8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from api import models
from api.utils import md5, monthlybill, monthlyinstanceconsumption, accountbalance, availableinstances


class AuthView(APIView):
    '''
    认证
    '''

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}

        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "user or password is error"
            #为用户创建token
            token = api.utils.md5(user)
            #存在就创建 不存在就更新
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token

        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return JsonResponse(ret)

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

class MonthlyInstanceConsumptionView(APIView):
    '''
    实例月账单详情查询
    '''

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            key_id = request._request.POST.get('key_id')
            key_secret = request._request.POST.get('key_secret')
            month = request._request.POST.get('month')
            pagenum = request._request.POST.get('pagenum')
            result = monthlyinstanceconsumption(key_id, key_secret, month, pagenum)

            result_total = []
            if result:
                for pagenums in range(2, int(result[0]['TotalNum']) + 1):
                    results = monthlyinstanceconsumption(key_id, key_secret, month, pagenum)
                    results.pop(0)
                    result_total.extend(results)
            result_total.extend(result)
            ret['data'] = {'TotalCount': result[0]['TotalCount'],
                           'Instancelist': result[1:]}
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = str(e)

        return JsonResponse(ret)

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

