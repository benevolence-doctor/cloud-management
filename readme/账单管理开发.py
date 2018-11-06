
	
 
   



接口文档：
1.每月业务线和不同环境消费情况
	1) 接口说明
		url: http://127.0.0.1:8000/api/v1/money/monthlysum/
		method: post
		传入参数说明: 
		business_line: 业务线 
			可选参数:
			all 全部
			smart 新智社区
			smart2 老智社区
			sqbj 社区半径
			msqbj 半径管家
			gigold 吉高支付
			zh 众海
			ding 钉钉
		env: 环境
			可选参数：
			all 
			sit 
			uat
			prod	
		billing_cycle: 结算周期
			可选参数：
			格式为：2018-08
	2) 接口示例
		例如：http://127.0.0.1:8000/api/v1/money/monthlysum/
		传入参数:{'business_line': 'ding', 'env': 'all', 'billing_cycle': '2018-09'}
		返回结果：
			{
			"code": 1000,
			"msg": null,
			"totals": [
				{
					"billing_cycle": "2018-09",
					"sum_money": 3509.023,
					"sum_num": 35
				}
			],
			"data": [
				{
					"billingCycle": "2018-09",
					"productName": "对象存储OSS",
					"businessLine": "ding",
					"env": "uat",
					"pretaxAmount": 0.01,
					"instanceTotals": 1
				},	...]}
			
2. 每月所有业务线的产品消费明细
    1) 接口说明
		url: http://127.0.0.1:8000/api/v1/money/monthlybillinfo/
		method: post
		传入参数说明:
		business_line: 同上
		env: 同上
		billingCycle:同上	
	2) 接口示例
		url: http://127.0.0.1:8000/api/v1/money/monthlybillinfo/
		传入参数:{'business_line': 'ding', 'env': 'all', 'billing_cycle': '2018-09'}
       返回结果:
		   {
			"code": 1000,
			"msg": null,
			"totals": {
				"billingCycle": "2018-09",
				"弹性公网IP": 7,
				"NAT网关": 1,
				"关系型数据库RDS": 2,
				"负载均衡SLB": 2,
				"云服务器ECS": 20,
				"云盘": 2
			},
			"data": [
				{
					"billingCycle": "2018-09",
					"productName": "弹性公网IP",
					"instanceId": "eip-bp14ckaaz7eqb6mfpozlv",
					"instanceName": "ding-prod-m1",
					"businessLine": "ding",
					"env": "prod",
					"subscriptionType": "后付费",
					"pretaxAmount": 0
				},
						
	
3. 阿里云账号剩余可用金额
	1) 接口说明
		url: http://127.0.0.1:8000/api/v1/money/accountbalance/
		method: get
	2) 接口示例
		url: http://127.0.0.1:8000/api/v1/money/accountbalance/
		返回解决：
		{
		"code": 1000,
		"msg": null,
		"data": [
			{
				"阿里云账号": "development@sqbj.com",
				"备注": "老智社区sit账号",
				"可用余额": "29,393.50"
			},...]}
	



