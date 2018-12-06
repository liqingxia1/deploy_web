# -*- coding: utf-8 -*-  
from h_box_deploy import H_BOX_Deploy
from sql_opt import Sql_Opt
import sys,os
import re
import time
import datetime

path = "/home/build/MK_OTA/"
 
paths = {}
paths["C8"] = path + "C8"
paths["C10"] = path + "C10"
paths["CPE02"] = path+ "CPE02"


def get_ota_names():
	'''
	获取每个项目下的所有版本名称与版本号
	'''
	# ota_all 存储所有ota需要的基本信息；以项目名称为key，存储版本的名称与版本号；dic类型中嵌入dic
	ota_all = {}
	for i in paths:
		ota_path = path+i+"/"+i+"_ota_package"
		# versions 存储**_ota_package路径下所有的文件名称；list类型
		versions = os.listdir(ota_path)
		# ota_versions 存储版本的名称与版本号，版本号为key，完整的名称为value；dic类型
		ota_versions = {}
		for version in versions:
			ota_version = str(re.findall(r"\d{1,2}\.\d{1,2}\.\d{1,3}",version))
			ota_version = ota_version.strip("']").strip("'[")
			ota_versions[str(ota_version)] = version
		ota_all[i] = ota_versions 
	return ota_all

 

def sort(ota_all):
	'''
	根据版本号进行排序
	'''
	# 遍历所有项目
	sort_ota = {}
	for i in ota_all:
		sort_version = []
		if len(ota_all[i])>0:
			for j in ota_all[i]:
				if len(j) >0:
					sort_version.append(j)
			sort_version = sorted(sort_version)
			sort_ota[i] = sort_version
	print sort_ota
	return sort_ota

ota_all = get_ota_names() 
sort_ota = sort(ota_all)


#浏览器登录操作
print "\n执行登录操作，请手动输入验证码"
web_opt = H_BOX_Deploy()
web_opt.login()


# 操作链接数据库
conn = Sql_Opt()
conn.connect()

for model in sort_ota:
	version = sort_ota[model][-1]
	model = model
	version_number = ota_all[model][version]

	#发布版本
	web_opt.open_channel_manage()
	if web_opt.released(version_number):
		print "\n发布"+model+","+version+"版本成功；版本名称为："+version_number +""
		conn.insert(model,"v"+version,version_number)
		# 浏览器上个版本的取消发布操作
		if model == "CPE02":
			number = 1
		else:
			number = 2
		last_version = version[:4] + str(int(version[4:])-number)
		print "\n取消发布状态的版本为："+last_version
		last_version_number = conn.select(model,"v"+last_version)
		print "查询数据库，要取消的版本信息为："
		print last_version_number
		web_opt.open_channel_manage()
		web_opt.unpublish(model,version,last_version,last_version_number)
		print "取消发布"+model+","+last_version+"版本成功"
		print "\n"
	else:
		print "\nERROR 发布"+model+","+version+"版本失败；版本名称为："+version_number 





