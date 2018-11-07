# -*- coding: utf8 -*-
from rest_framework import serializers
from api import models

class EcsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EcsInfo
        fields = '__all__'

class RdsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RdsInfo
        fields = '__all__'

class SlbInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlbInfo
        fields = '__all__'

class EipInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EipInfo
        fields = '__all__'

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

class MonthlybillInfoSerializer(serializers.ModelSerializer):
    billingCycle = serializers.CharField(max_length=255)
    productName = serializers.CharField(max_length=255)
    instanceId = serializers.CharField(max_length=255)
    instanceName = serializers.CharField(max_length=255)
    businessLine = serializers.CharField(max_length=255)
    env = serializers.CharField(max_length=255)
    subscriptionType = serializers.CharField(max_length=255)
    pretaxAmount = serializers.FloatField()

    class Meta:
        model = models.MonthlybillInfo
        fields = ['billingCycle', 'productName', 'instanceId', 'instanceName',
                  'businessLine', 'env', 'subscriptionType','pretaxAmount']

