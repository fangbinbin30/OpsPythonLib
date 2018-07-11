#!/local/bin/env python
# -*- coding:utf8 -*-
# Fangbinbin

import json
import urllib.request

##关键参数变量默认值
ZabbixName = "Admin"
ZabbixPassword = "密码"
ZabbixUrl = "http://IP地址/zabbix/api_jsonrpc.php"
ZabbixHeader = {"Content-Type":"application/json"}


class ConnZabbix:  ##连接Zabbix对象
	def __init__(self,ZabbixName=ZabbixName,ZabbixPassword=ZabbixPassword,ZabbixUrl=ZabbixUrl,ZabbixHeader=ZabbixHeader):
		self.ZabbixName = ZabbixName
		self.ZabbixPassword = ZabbixPassword
		self.ZabbixUrl = ZabbixUrl
		self.ZabbixHeader = ZabbixHeader
		self.authID = self.Login()

	def Login(self,userData=False):
		data = {
			"jsonrpc": "2.0",
			"method": "user.login",
			"params":{
				"user": self.ZabbixName,
				"password": self.ZabbixPassword,
				"userData": userData
			},
			"id": 1
		}
		LoginResponse = self.SelectZabbix(data)
		return LoginResponse['result']

	def GetHosts(self,hostname):
		data = {
			"jsonrpc": "2.0",
			"method": "host.get",
			"params": {
				"output":"extend",
				#"output": ["hostid","name","host"],
				"search": {
					"name": hostname
				},
			},
			"id": 2,
			"auth": self.authID
		}
		getHostinfo = self.SelectZabbix(data)
		return getHostinfo["result"][0]

	def GetApplication(self,hostid,AppName="Health"):
		data = {
			"jsonrpc": "2.0",
			"method": "application.get",
			"params": {
				"output": "extend",
				"hostids": hostid,
				"filter": {
					"name": AppName
				}
			},
			"auth": self.authID,
			"id":3
		}
		getApplicationInfo = self.SelectZabbix(data)
		return getApplicationInfo["result"][0]

	def GetItem(self,hostid):
		data = {
			"jsonrpc": "2.0",
			"method": "item.get",
			"params": {
				"output": "extend",
				"hostids": hostid,
				"sortfield": "name"
			},
			"auth": self.authID,
			"id": 4
		}
		getItem = self.SelectZabbix(data)
		return getItem["result"]
##创建监控项
	def CreateItem(self,projectName,hostname,project_management_port,hostid,appid):
		data = {
			"jsonrpc": "2.0",
			"method": "item.create",
			"params": {
				"name": "{}_metrics检查".format(projectName),
				"key_": "metrics_check[{},{}]".format(hostname,project_management_port),
				"hostid": hostid,
				"type": 7,
				"value_type": 3,
				 # "interfaceid": "30084",
				"applications": ["{}".format(appid)],
				"delay": "2m"
			},
			"auth": self.authID,
			"id": 4
		}
		createIteminfo = self.SelectZabbix(data)
		return createIteminfo["result"][0]

	def GetTriger(self,hostid):
		data = {
			"jsonrpc": "2.0",
			"method": "trigger.get",
			"params": {
				"hostids":hostid,
				"output": "exend",
				"filter": {
					"priority": 5,
					"description": "{HOST.NAME} 宕机"
				},
			},
			"auth": self.authID,
			"id":5
		}
		gettrigerinfo = self.SelectZabbix(data)
		return gettrigerinfo["result"][0]

##创建触发器
	def CreateTriger(self,projectName,host,hostname,project_management_port,deptriid):
		data = {
			"jsonrpc": "2.0",
			"method": "trigger.create",
			"params": [
				{
					"description": "{}:metrics检查异常".format(projectName),
					"expression": "{{{}:metrics_check[{},{}].avg(#2)}}<>200".format(host,hostname,project_management_port),
					"priority":"4",
					"dependencies":[{"triggerid",deptriid}]
				}
			],
			"auth": self.authID,
			"id": 6
		}
		createtriger = self.SelectZabbix(data)
		return createtriger



	def SelectZabbix(self,SelectData):
		request = urllib.request.Request(url=self.ZabbixUrl,headers=self.ZabbixHeader,data=json.dumps(SelectData).encode())
		result = urllib.request.urlopen(request)
		response = json.loads(result.read())
		result.close()
		#print("hostdatainfo:{}".format(response))
		print(response['result'])
		return response



if "__main__" == __name__:
	zabapi = ConnZabbix(ZabbixName,ZabbixPassword,ZabbixUrl,ZabbixHeader)
	print(zabapi.authID)
	hostid = zabapi.GetHosts("10.0.100.6").get("hostid")
	applicationid = zabapi.GetApplication(hostid).get("applicationid")

	x = applicationid
	print(x)