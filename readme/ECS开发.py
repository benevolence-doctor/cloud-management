ECS开发文档说明
1. 获取所有ECS实例列表
	url: http://127.0.0.1:8000/api/v1/money/ecsinfo
	method: get
	返回结果：
		{
			"code": 1000,
			"msg": null,
			"data": [
				{
					"id": 1,
					"instanceId": "i-uf64rxfgaum7snfzh3u3",
					"instanceName": "smart2-sit-w4",
					"productCode": "ecs",
					"businessLine": "smart2",
					"env": "sit",
					"regionId": "cn-shanghai",
					"status": "Running",
					"instanceNetworkType": "vpc",
					"publicIpAddress": "",
					"primaryIpAddress": "10.10.7.37",
					"cpuMemory": "2vCpu 16.0G",
					"osType": "linux",
					"osName": "CentOS  7.3 64位",
					"hostname": "dev-docker-worker04",
					"yunDisk": "[100]",
					"creationTime": "2018-07-12T07:03Z",
					"expiredTime": "2018-12-12T16:00Z",
					"remark": ""
				},...]}

2. 获取单个ECS实例详细信息
	url: http://127.0.0.1:8000/api/v1/money/ecsinfo/(+d)/
	method: get
	返回结果：
		{
			"code": 1000,
			"msg": null,
			"data": [
				{
					"id": 1,
					"instanceId": "i-uf64rxfgaum7snfzh3u3",
					"instanceName": "smart2-sit-w4",
					"productCode": "ecs",
					"businessLine": "smart2",
					"env": "sit",
					"regionId": "cn-shanghai",
					"status": "Running",
					"instanceNetworkType": "vpc",
					"publicIpAddress": "",
					"primaryIpAddress": "10.10.7.37",
					"cpuMemory": "2vCpu 16.0G",
					"osType": "linux",
					"osName": "CentOS  7.3 64位",
					"hostname": "dev-docker-worker04",
					"yunDisk": "[100]",
					"creationTime": "2018-07-12T07:03Z",
					"expiredTime": "2018-12-12T16:00Z",
					"remark": ""
					]}
    
	