ECS开发文档说明
1. 获取此账号下所有ECS实例列表
	url: http://guoj.sqbj.com/api/v1/ecs
	{
    "code": 1000, 正常返回值1000 若异常返回1002
    "msg": null,
    "data":
        "TotalCount": 43,
        "Instancelist": [
        {
         "产品名称": "云服务器ECS",
         "实例ID": " ",
         "实例名称": 
         "实例网络类型": " ", #vpc:VPC classic:经典网络
         "实例公网地址": " ",
         "实例内网地址": " ",
		 "实例状态": "",
         "付费方式": " ",
         "实例地域ID": " ",
         "实例配置"："2 vCPU 16 GB",
		 "实例系统类型"： linux,
		 "实例系统版本"："CentOS 7.3 64位",
		 "实例主机名"：HostName
         "创建时间": " ",
         "过期时间": " "
         },
		 {
		     .....
		 }]
    }

2. 获取单个ECS实例详细信息
	url: http://guoj.sqbj.com/api/v1/ecs/(+d)/
	{
    "code": 1000, 正常返回值1000 若异常返回1002
    "msg": null,
    "data":
        "Instancelist": [
        {
         "产品名称": "云服务器ECS",
         "实例ID": " ",
         "实例名称": 
         "实例网络类型": " ", #vpc:VPC classic:经典网络
         "实例公网地址": " ",
         "实例内网地址": " ",
		 "实例状态": "",
         "付费方式": " ",
         "实例地域ID": " ",
         "实例配置"："2 vCPU 16 GB",
		 "实例系统类型"： linux,
		 "实例系统版本"："CentOS 7.3 64位",
		 "实例主机名"：HostName
         "创建时间": " ",
         "过期时间": " "
         }]
    
	