# -*- coding: utf-8 -*-   
from h_box_deploy import H_BOX_Deploy
from send_mail import Send_Mail
import sys,os
import re
import time
import datetime

path = "/home/build/MK_OTA/"
paths = {}
paths["C8"] = path + "C8"
paths["C10"] = path + "C10"
paths["CPE02"] = path+ "CPE02"
country = ["NCA","KHM"]


def get_ota_names(identifier):
	'''
	获取每个项目下的所有版本名称与版本号
	'''
	print identifier
	
	# ota_all 存储所有ota需要的基本信息；以项目名称为key，存储版本的名称与版本号；dic类型中嵌入dic
	ota_all = {}
	# 根据输入的identifier进行项目升级差分包
	if identifier == 'CPE02':
		ota_path = path+"CPE02/CPE02_ota_package" 
	else:
		model = identifier.replace("_NCA", '').replace('_KHM', '')
		country = identifier.replace("C8_", '').replace('C10_', '')
		ota_path = path+model+"/"+model+"_ota_package/" +country
	# ota_versions 存储版本的名称与版本号，版本号为key，完整的名称为value；dic类型
	versions = os.listdir(ota_path)
	ota_versions = {}
	for version in versions:
		ota_version = str(re.findall(r"\d{1,2}\.\d{1,2}\.\d{1,3}",version))
		ota_version = ota_version.strip("']").strip("'[")
		ota_versions[str(ota_version)] = version
	ota_all[identifier] = ota_versions
	return ota_all

 

def sort(ota_all):
	
	'''
	根据版本号进行排序
	'''
	# 遍历所有项目
	print "根据版本号进行排序"
	sort_ota = {}
	for i in ota_all:
		sort_version = []
		if len(ota_all[i])>0:
			for j in ota_all[i]:
				if len(j) >0:
					sort_version.append(j)
			numbers = []
			for sort in sort_version:
				number = re.findall(r"\d{1,3}",sort)
				numbers.append(number[2])
			for a in range(1,len(numbers)):
				for b in range(0,len(numbers) - a):
					if int(numbers[b]) > int(numbers[b+1]):
						numbers[b], numbers[b+1] = numbers[b+1], numbers[b]
			sort_version = numbers
			start = re.findall(r"\d{1,3}",sort)
			sort_versions = []
			for sort in sort_version:
				a =  str(start[0])+'.'+str(start[1])+'.'+str(sort)
				sort_versions.append(a)
			sort_ota[i] = sort_versions 
	print "排序后版本号：",sort_ota
	return sort_ota

def build_ota(ota_all, sort_ota):
	update = {}
	for i in sort_ota:
		model = i.replace("_NCA", '').replace('_KHM', '')
		country = i.replace("C8_", '').replace('C10_', '')
		update_versions = {}
		end_version = sort_ota[i][-1]
		end_ota_name = ota_all[i][sort_ota[i][-1]]
		out_path = path+"Dif_packet/"+i+"/"+end_version+"/"
		os.system("mkdir "+out_path)
		for j in sort_ota[i][:-1]:
			start_ota_name = ota_all[i][j]
			update_name = i+"_update"+j+"-"+end_version+".zip"
			update_versions[j] = update_name
			#print start_ota_name,end_version,update_name ,update_versions[j]
			# 执行差分成操作语句，若已生成查分包，可注释os.system语句
			print 'end_version',end_version
			print model,country
			if i == "CPE02":
				print "./build/tools/releasetools/ota_from_target_files -v -i ./"+i+"_ota_package/"+start_ota_name+"/msm8909_512-target_files-eng.build.zip ./"+i+"_ota_package/"+end_ota_name+"/msm8909_512-target_files-eng.build.zip "+ out_path + update_name
				#os.system("cd "+paths[i]+"; pwd; ./build/tools/releasetools/ota_from_target_files -v -i ./"+i+"_ota_package/"+start_ota_name+"/msm8909_512-target_files-eng.build.zip ./"+i+"_ota_package/"+end_ota_name+"/msm8909_512-target_files-eng.build.zip "+path+" Dif_packet/"+i+"/"+update_name)
				pass
			else:
				print "./build/tools/releasetools/ota_from_target_files -v -2 -i ./"+model+"_ota_package/"+country+"/"+start_ota_name+"/msm8952_64-target_files-eng.build.zip ./"+model+"_ota_package/"+country+"/"+end_ota_name+"/msm8952_64-target_files-eng.build.zip "+out_path + update_name
				#os.system("cd "+paths[model]+"; pwd; ./build/tools/releasetools/ota_from_target_files -v -2 -i ./"+model+"_ota_package/"+country+"/"+start_ota_name+"/msm8952_64-target_files-eng.build.zip ./"+model+"_ota_package/"+country+"/"+end_ota_name+"/msm8952_64-target_files-eng.build.zip "+out_path + update_name)
				pass
		update[i] = update_versions
	print update
	return update, out_path

def get_time():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def build_run(identifier):
	otatime = {}

	otatime["start"] = get_time()
	print "\n开始时间" + otatime["start"]

	# 浏览器登录操作
	print "执行登录操作，请手动输入验证码，无需点击登录按钮"
	web_opt = H_BOX_Deploy()
	web_opt.login()

	# 差分包生成操作
	ota_all = get_ota_names(identifier)
	sort_ota = sort(ota_all)
	# print "=======开始生成差分包========"
	otatime["build_str_time"] = get_time()
	update, update_path = build_ota(ota_all, sort_ota)
	otatime["build_end_time"] = get_time()
	# print "=======end 差分包生成完成========"
	time.sleep(3)

	# 打开time.txt文件，写入操作的时间点
	fo = open("time.txt", "w")
	fo.write("开始时间：" + otatime["start"] + "\n")
	fo.write("开始生成差分包时间：" + otatime["build_str_time"] + "\n")
	fo.write("结束生成差分包时间：" + otatime["build_end_time"] + "\n")

	version_name = ""
	mail_msg = []
	for model in sort_ota:
		print "\n开始执行浏览器的新增版本与上传操作\n\n"
		# 浏览器的上传操作
		print update[model]
		otatime[model + "add_version_time"] = get_time()
		version_name = ota_all[model][sort_ota[model][-1]]
		print model, version_name, sort_ota[model][-1]
		a = sort_ota[model][-1][:4] + str(int(sort_ota[model][-1][4:]) - 1)
		print a
		opt_model = model.replace("_NCA", '').replace('_KHM', '')
		if web_opt.start(opt_model, version_name):
			# 继续写入操作时间点
			fo.write("\nweb-新建项目开始时间：" + otatime[model + "add_version_time"] + "\n")
			for j in sort_ota[model][:-1]:
				otatime[model + j + "add_str_ota_time"] = get_time()
				update_name = update[model][j]
				print j, path + "Dif_packet/" + model + "/" + update_name
				web_opt.add_difference_package(j, update_path + update_name)
				time.sleep(5)
				print "差分包:" + update_name + "上传完成"
				otatime[model + j + "add_end_ota_time"] = get_time()
				mail_msg.append(update_name)
				# 继续写入操作时间点
				fo.write("web-" + model + "上传差分包" + j + "开始时间：" + otatime[model + j + "add_str_ota_time"] + "\n")
				fo.write("web-" + model + "上传差分包" + j + "完成时间：" + otatime[model + j + "add_end_ota_time"] + "\n")
	print "\n\n结束浏览器的操作\n"

	otatime["end"] = get_time()
	print "\n结束时间" + otatime["end"] + "\n\n"
	fo.write("结束时间:" + otatime["end"] + "\n")
	fo.close()

	# 根据上传完成的差分包版本，发邮件通知到测试
	if len(mail_msg):
		mail = Send_Mail()
		mail.start(mail_msg, version_name)

	return web_opt














