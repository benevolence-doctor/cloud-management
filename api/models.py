from django.db import models


class UserInfo(models.Model):
    user_choices = (
        (1, "普通用户"),
        (2, "VIP"),
        (3, "SVIP"),

    )

    user_type = models.IntegerField(choices=user_choices, default=1)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

class BusinessLine(models.Model):
    ''' 业务线不同环境信息 '''

    env = models.CharField(db_column='env', max_length=255, default='sit')
    businessLine = models.CharField(db_column='business_line', max_length=255)
    remark = models.CharField(db_column='remark', max_length=1024)

    def __str__(self):
        return self.env

class KeyIdSecret(models.Model):
    '''阿里云账号信息'''

    keyId = models.CharField(db_column='key_id', max_length=255, null=False)
    keySecret = models.CharField(db_column='key_secret', max_length=255, null=False)
    regionId = models.CharField(db_column='region_id', max_length=1024)
    accountNumber = models.CharField(db_column='account_number', max_length=1024)
    defaultEnv = models.CharField(db_column='default_env', max_length=255)
    remark = models.CharField(db_column='remark', max_length=1024)

    def __str__(self):
        return self.keyId

class ProductName(models.Model):
    '''
    产品code 商品name 商品code 备注'''

    productcode = models.CharField(max_length=255, null=False)
    commodityname = models.CharField(max_length=255)
    commoditycode = models.CharField(max_length=255)
    remark = models.CharField(max_length=1024)

    def __str__(self):
        return self.commodityname

class EcsInfo(models.Model):
    ''' ECS服务器信息列表 '''


    #实例ID
    instanceId = models.CharField(db_column='instance_id', max_length=255, null=False)
    #实例名称
    instanceName = models.CharField(db_column='instance_name', max_length=255)
    #产品code
    productCode = models.CharField(db_column='product_code', max_length=255)
    #实例业务线
    businessLine = models.CharField(db_column='business_line', max_length=255)
    #实例环境
    env = models.CharField(db_column='env', max_length=255)
    #实例地域ID
    regionId = models.CharField(db_column='region_id', max_length=255)
    #实例状态
    status = models.CharField(db_column='status', max_length=255)
    #实例网络类型
    instanceNetworkType = models.CharField(db_column='instance_networktype', max_length=255)
    #实例公网地址
    publicIpAddress = models.CharField(db_column='public_ipaddress', max_length=255)
    #实例内网地址
    primaryIpAddress = models.CharField(db_column='primary_ipaddress', max_length=255)
    #实例配置 (2 vCPU 16 GB)
    cpuMemory = models.CharField(db_column='cpu_memory', max_length=255)
    #实例系统类型
    osType = models.CharField(db_column='os_type', max_length=255)
    #实例系统版本
    osName = models.CharField(db_column='os_name', max_length=255)
    #实例主机名
    hostname = models.CharField(db_column='hostname', max_length=255)
    #云盘大小(调用yundisk的类)
    yunDisk = models.CharField(db_column='yundisk', max_length=255)
    #创建时间
    creationTime = models.CharField(db_column='create_time',max_length=255)
    #过期时间
    expiredTime = models.CharField(db_column='expired_time', max_length=255)
    #备注
    remark = models.CharField(db_column='remark', max_length=255)

    def __str__(self):
        return self.instanceId

class RdsInfo(models.Model):
    ''' RDS实例列表 '''

    #实例ID
    instanceId = models.CharField(db_column='instance_id', max_length=255, null=False)
    #实例名称
    instanceName = models.CharField(db_column='instance_name', max_length=255)
    #产品code
    productCode = models.CharField(db_column='product_code', max_length=255)
    #实例业务线
    businessLine = models.CharField(db_column='business_line', max_length=255)
    #实例环境
    env = models.CharField(db_column='env', max_length=255)
    #实例地域ID
    regionId = models.CharField(db_column='region_id', max_length=255)
    #实例状态
    status = models.CharField(db_column='status', max_length=255)
    #实例网络类型
    instanceNetworkType = models.CharField(db_column='instance_networktype', max_length=255)
    #实例公网地址
    publicIpAddress = models.CharField(db_column='public_ipaddress', max_length=255)
    #实例内网地址
    primaryIpAddress = models.CharField(db_column='primary_ipaddress', max_length=255)
    #实例配置 (2 vCPU 16 GB)
    cpuMemory = models.CharField(db_column='cpu_memory', max_length=255)
    #数据库类型
    engine = models.CharField(db_column='engine', max_length=255)
    #实例类型
    instanceType = models.CharField(db_column='instance_type', max_length=255)
    #主实例的ID
    masterInstanceId = models.CharField(db_column='master_instanceid', max_length=255)
    #灾备实例ID
    guardDBInstanceId = models.CharField(db_column='guarddb_instanceid', max_length=255)
    #只读实例ID
    readOnlyDBInstanceId = models.CharField(db_column='readonlydb_instanceid', max_length=255)
    #创建时间
    creationTime = models.CharField(db_column='create_time',max_length=255)
    #过期时间
    expiredTime = models.CharField(db_column='expired_time', max_length=255)
    #备注
    remark = models.CharField(db_column='remark', max_length=255)

    def __str__(self):
        return self.instanceId

class SlbInfo(models.Model):
    '''SLB实例列表'''

    #实例ID
    instanceId = models.CharField(db_column='instance_id', max_length=255, null=False)
    #实例名称
    instanceName = models.CharField(db_column='instance_name', max_length=255)
    #产品code
    productCode = models.CharField(db_column='product_code', max_length=255)
    #实例业务线
    businessLine = models.CharField(db_column='business_line', max_length=255)
    #实例环境
    env = models.CharField(db_column='env', max_length=255)
    #实例地域ID
    regionId = models.CharField(db_column='region_id', max_length=255)
    #实例状态
    status = models.CharField(db_column='status', max_length=255)
    #实例网络类型
    instanceNetworkType = models.CharField(db_column='instance_networktype', max_length=255)
    #四层协议或七层协议
    internetChargeType = models.CharField(db_column='internet_chargeType', max_length=255)
    #实例IP地址
    ipaddress = models.CharField(db_column='ipaddress', max_length=255)
    #后端服务组
    BackendServers = models.CharField(db_column='backend_servers', max_length=255)
    #监听协议和端口
    ListenPorts = models.CharField(db_column='listen_ports', max_length=255)
    #创建时间
    creationTime = models.CharField(db_column='create_time',max_length=255)
    #过期时间
    expiredTime = models.CharField(db_column='expired_time', max_length=255)
    #备注
    remark = models.CharField(db_column='remark', max_length=255)

    def __str__(self):
        return self.instanceId

class EipInfo(models.Model):
    '''弹性公网EIP实例列表'''

    #实例ID
    allocationId = models.CharField(db_column='allocation_id', max_length=255, null=False)
    #实例名称
    allocationName = models.CharField(db_column='allocation_name', max_length=255)
    #使用此实例的产品ID
    instanceId = models.CharField(db_column='instance_id', max_length=255)
    #使用此实例的产品类型
    instanceType = models.CharField(db_column='instance_type', max_length=255)
    #产品code
    productCode = models.CharField(db_column='product_code', max_length=255)
    #实例业务线
    businessLine = models.CharField(db_column='business_line', max_length=255)
    #实例环境
    env = models.CharField(db_column='env', max_length=255)
    #实例地域ID
    regionId = models.CharField(db_column='region_id', max_length=255)
    #实例状态
    status = models.CharField(db_column='status', max_length=255)
    #实例IP地址
    ipaddress = models.CharField(db_column='ipaddress', max_length=255)
    #创建时间
    creationTime = models.CharField(db_column='create_time',max_length=255)
    #过期时间
    expiredTime = models.CharField(db_column='expired_time', max_length=255)
    #备注
    remark = models.CharField(db_column='remark', max_length=255)

    def __str__(self):
        return self.allocationId

class MonthlybillInfo(models.Model):
    '''月账单实例详细信息'''

    billingCycle = models.CharField(db_column='month', max_length=255)
    productCode = models.CharField(db_column='product_code', max_length=255)
    productName = models.CharField(db_column='product_name', max_length=255)
    instanceId = models.CharField(db_column='instance_id', max_length=255)
    instanceName = models.CharField(db_column='instance_name', max_length=255)
    businessLine = models.CharField(db_column='business_line', max_length=255)
    env = models.CharField(db_column='env', max_length=255)
    regionId = models.CharField(db_column='region_id', max_length=255)
    status = models.CharField(db_column='status', max_length=255)
    subscriptionType = models.CharField(db_column='subscription_type', max_length=255)
    pretaxAmount  = models.FloatField(db_column='pretax_amount', max_length=255)
    remark = models.CharField(db_column='remark', max_length=255)

    def __str__(self):
        return  self.instanceId

class MonthlySum(models.Model):
    '''月账单汇总信息'''

    billingCycle = models.CharField(db_column='month', max_length=255)
    productName = models.CharField(db_column='product_name', max_length=255)
    businessLine = models.CharField(db_column='business_line', max_length=255)
    env = models.CharField(db_column='env', max_length=255)
    pretaxAmount = models.FloatField(db_column='pretax_amount', max_length=255)
    instanceTotals = models.IntegerField(db_column='instance_totals')
    remark = models.CharField(db_column='remark', max_length=255)

    def __str__(self):
        return  self.productName
