1. 业务线
   1) 表名: business_line
   2) 表结构如下(字段名称 说明)：
	   id
	   business 业务线
	   env      环境
	   key_id  Access Key ID
	   key_secret Access Key Secret 
	   region_id  Region-ID
	   remark   备注
2.  产品code
	1) 表名 productcode_name
	2) 表结构
		id
		productcode 产品code
		merchandisecode 商品code
		merchandisename 商品名称
3.  计费方式
   1) 表名 instance_charge_type
   2) 表结构
		id
		预付费
		后付费	
4.  1) 获取所有实例的基本信息 
	  表名：monthlybill
	   表结构：
	   id
	   产品code
	   产品名称
	   实例id
	   实例名称
	   Region
	   状态
	   业务线
	   环境
	   付费方式
	   付费金额
	   备注
	2) 业务线和环境下各个产品的消费总额
		表名：monthlysum
		表结构：
		id
		产品名称
		业务线
		环境
		付费金额
		备注
		
	
	
   
5. 不同产品不同表
	1. 获取ECS实例的基本信息(DescribeInstanceAttribute)
		表名: ecsinfo
		表结构:
		InstanceId 实例ID
		InstanceName 实例名称
		Productcode  产品名称
		BusinessLine 实例业务线
		Env 实例环境
		RegionId 实例地域ID
		Status 实例状态
		InstanceNetworkType 实例网络类型
		PublicIpAddress 实例公网地址
		PrimaryIpAddress 实例内网地址
		CpuMemory 实例配置 (2 VCPU 16 GB)
		OSType 实例系统类型
		OSName 实例系统版本
		HostName 实例主机名
		YunDisk 云盘大小(调用yundisk的类)##############
		CreationTime 创建时间
		ExpiredTime 过期时间
		Remark 备注
		
	2. 获取RDS实例的基本信息(DescribeDBInstanceAttribute)
		表名：rdsinfo
		表结构：
		InstanceId 实例ID
		InstanceName 实例名称(DBInstanceDescription)
	    Productcode  产品名称
		BusinessLine 实例业务线
		Env 实例环境
		RegionId 实例地域ID
		Status 实例状态(DBInstanceStatus)
		Engine 数据库类型(Engine EngineVersion)
		CpuMemory 实例配置 （2 vCPU 16 GB ）
		InstanceNetworkType 实例网络类型
		PublicIpAddress 实例公网地址 (DescribeDBInstanceNetInfo需要这个类)
		PrimaryIpAddress 实例内网地址(ConnectionString)
		InstanceType 实例类型（Primary：主实例 Readonly：只读实例 Guard：灾备实例）
		MasterInstanceId 主实例的ID
		GuardDBInstanceId 灾备实例ID
		ReadOnlyDBInstanceId 只读实例ID
		CreationTime 创建时间
		ExpiredTime 过期时间
		Remark 备注
		
	3. 获取SLB实例的基本信息(DescribeLoadBalancerAttribute)
		表名：slbinfo
		表结构：
		InstanceId 实例ID(LoadBalancerId)
		InstanceName 实例名称(LoadBalancerName)
	    Productcode  产品名称
		BusinessLine 实例业务线
		Env 实例环境
		RegionId 实例地域ID(RegionIdAlias)
		Status 实例状态()
		PublicIpAddress 实例公网地址 (调用EIP类获取)#################
		PrimaryIpAddress 实例内网地址(Address)
		BackendServers 后端服务组(BackendServers ServerId 调用ECS的类获取ServerName)###############
		ListenPorts 监听端口组
		CreationTime 创建时间
		ExpiredTime 过期时间
		Remark 备注

	4. 获取云盘实例的基本信息(DescribeDisks)
	    表名: yundiskinfo
		表结构:
		InstanceId 实例ID(DiskId)
		InstanceName 挂载ECS实例ID(InstanceId)
		Size 云盘大小(Size)
	    Remark 备注
		
	5. 获取弹性公网EIP的基本信息(DescribeEipAddresses)
		表名: eipinfo
		表结构:
		AllocationId 实例ID(AllocationId)
		InstanceName 实例NAME(LoadBalancerName)
		InstanceType 使用此实例的产品类型(InstanceType 如:SlbInstance Nat)
		InstanceId 使用此实例的产品ID
		Status 实例状态(Status)
		IpAddress 实例的IP地址(IpAddress)
		RegionId 实例区域ID(RegionId)
		BusinessLine 实例业务线
		Env 实例环境
	    AllocationTime 实例创建时间(AllocationTime)
		Remark 备注
	
	6. 获取NAT的基本信息(DescribeNatGateways)
		表名: natinfo
		表结构:
		InstanceId 实例ID(NatGatewayId)
		CreationTime 创建时间
		Name 实例名称
		Status 状态
		Spec 实例规格
		RegionId 实例区域ID
		IPaddress: 实例公网地址(调用弹性公网EIP类) ###########
		InstanceChargeType 实例付费方式
	    Remark 备注
	7. 
	
	
	
	
	
	
	
	
	
	
	
	