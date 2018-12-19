# -*- coding: utf-8 -*-  
from h_box_deploy import H_BOX_Deploy
from sql_opt import Sql_Opt
from build_package import *
import sys,os
import re
import time
import datetime



def released_run(identifier):

	#浏览器登录操作
	print "\n执行登录操作，请手动输入验证码，无需点击登录按钮"
	web_opt = H_BOX_Deploy()
	web_opt.login()
	run(identifier, web_opt)


def released2_run(identifier,web_opt):
	run(identifier, web_opt)



def run(identifier,web_opt):
	ota_all = get_ota_names(identifier)
	sort_ota = sort(ota_all)
	print(sort_ota)

	# 操作链接数据库
	conn = Sql_Opt()
	conn.connect()

	for model in sort_ota:
		version = sort_ota[model][-1]
		change_model = model.replace("_NCA", '').replace('_KHM', '')
		version_number = ota_all[model][version]

		print "version_number: ", version_number



		#发布版本
		web_opt.open_channel_manage()
		if web_opt.released(version_number):
		#if True:
			print "\n发布"+change_model+","+version+"版本成功；版本名称为："+version_number +""
			conn.insert(change_model,"v"+version,version_number)
			# 浏览器上个版本的取消发布操作
			if model == "CPE02":
				number = 1
			else:
				number = 2
			last_version = version[:4] + str(int(version[4:])-number)
			print last_version
			print "\n取消发布状态的版本为："+last_version
			last_version_number = conn.select(change_model,"v"+last_version)
			print "查询数据库，要取消的版本信息为：",last_version_number
			web_opt.open_channel_manage()
			web_opt.unpublish(change_model,version,last_version,last_version_number)
			print "取消发布"+change_model+","+last_version+"版本成功"
			print "\n"
		else:
			print "\nERROR 发布"+model+","+version+"版本失败；版本名称为："+version_number





