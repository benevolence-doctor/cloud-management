RDS开发说明
1.获取账号下所有RDS实例列表
    url:http://127.0.0.1:8000/api/v1/money/rdsinfo
	method: get
	返回结果：
		{
			"code": 1000,
			"msg": null,
			"data": [
				{
					"id": 1,
					"instanceId": "rm-uf6fm08721ioc735k",
					"instanceName": "smart2-uat-rds",
					"productCode": "rds",
					"businessLine": "smart2",
					"env": "uat",
					"regionId": "cn-shanghai",
					"status": "Running",
					"instanceNetworkType": "VPC",
					"publicIpAddress": "rm-uf6fm08721ioc735klo.mysql.rds.aliyuncs.com",
					"primaryIpAddress": "rm-uf6fm08721ioc735k.mysql.rds.aliyuncs.com",
					"cpuMemory": "1CPU 1GB",
					"engine": "MySQL 5.6",
					"instanceType": "Primary",
					"masterInstanceId": "",
					"guardDBInstanceId": "",
					"readOnlyDBInstanceId": "",
					"creationTime": "2017-12-04T16:20Z",
					"expiredTime": "2018-12-04T16:00:00Z",
					"remark": ""
				},...]}

2.根据RDS实例ID获取RDS实例详细信息
	url: http://127.0.0.1:8000/api/v1/money/rdsinfo/(+d)/
	method: get
	返回结果：
		{
			"code": 1000,
			"msg": null,
			"data": [
				{
					"id": 1,
					"instanceId": "rm-uf6fm08721ioc735k",
					"instanceName": "smart2-uat-rds",
					"productCode": "rds",
					"businessLine": "smart2",
					"env": "uat",
					"regionId": "cn-shanghai",
					"status": "Running",
					"instanceNetworkType": "VPC",
					"publicIpAddress": "rm-uf6fm08721ioc735klo.mysql.rds.aliyuncs.com",
					"primaryIpAddress": "rm-uf6fm08721ioc735k.mysql.rds.aliyuncs.com",
					"cpuMemory": "1CPU 1GB",
					"engine": "MySQL 5.6",
					"instanceType": "Primary",
					"masterInstanceId": "",
					"guardDBInstanceId": "",
					"readOnlyDBInstanceId": "",
					"creationTime": "2017-12-04T16:20Z",
					"expiredTime": "2018-12-04T16:00:00Z",
					"remark": ""
				}
			]}
