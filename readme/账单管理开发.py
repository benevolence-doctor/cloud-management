
	
 
   



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
		billingCycle: 结算周期
			可选参数：
			格式为：2018-08
	2) 接口示例
		例如：http://127.0.0.1:8000/api/v1/money/monthlysum/
		传入参数:{'business_line': 'ding', 'env': 'all', 'billingCycle': '2018-09'}
		返回结果：
			{
			"code": 1000,
			"msg": null,
			"totals": [
				{
					"billingCycle": "2018-09",
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
		
2. 当前阿里云账号剩余可用金额
	1) 接口说明：
	2) 接口示例
	
2. 每月所有业务线的产品消费明细
    url: http://guoj.sqbj.com/api/v1/monthlyinstanceconsumption
	传入参数：env=all
3. 每月所有业务线剩余可用金额
	
3. 每月单个业务线消费总览
	url: http://guoj.sqbj.com/api/v1/monthlybill/(+d)/
4. 每月单个业务线的产品消费明细
	url: http://guoj.sqbj.com/api/v1/monthlyinstanceconsumption/(+d)/

	
5. 每月单个业务线不同环境消费总览
	url: http://guoj.sqbj.com/api/v1/monthlybill/(+d)/(+D)/
	url: http://guoj.sqbj.com/api/v1/monthlyinstanceconsumption/(+d)/(+D)/
6. 每月单个业务线不同环境消费明细




