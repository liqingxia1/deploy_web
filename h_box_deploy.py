# -*- coding: utf-8 -*-
import pyautogui
import os,sys,re
from selenium import webdriver
import pyperclip
from selenium.webdriver.support.ui import Select
import time

class H_BOX_Deploy:
	def __init__(self):
		self.driver = ""
		self.path = os.getcwd()
		self.path = sys.path[0]
		reload(sys)
		sys.setdefaultencoding('utf-8')

	def login(self, url="http://fota.redstone.net.cn/", username="******", password="******"):
		# 打开网页并执行登录，验证码需手动输入
		self.driver = webdriver.Firefox()
		self.driver.maximize_window()
		self.driver.get(url)
		self.driver.find_element_by_xpath('//*[@id="form"]/a[1]').click()
		self.driver.find_element_by_id("username").send_keys(username)
		self.driver.find_element_by_id("password").send_keys(password)
		time.sleep(10)
		self.driver.find_element_by_xpath('//*[@id="form"]/input').click()
		self.driver.implicitly_wait(60)  # 隐性等待，最长等30秒


	def open_channel_manage(self):
		# 进入渠道管理界面
		self.driver.find_element_by_class_name("se7en-gear").click()
		self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/ul/li[4]/ul/li[1]/a').click()

		# 点击新增渠道，并调用新增渠道界面的方法，进入到 固件管理 界面
		self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[3]/a').click()
		self.driver.implicitly_wait(60)  # 隐性等待，最长等30秒
	

	def add_firmware(self, versions, model ):
		# 点击新增固件
		self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[1]/div/form/div/div[1]/a').click()
		self.driver.implicitly_wait(60)  # 隐性等待，最长等30秒
		self.driver.find_element_by_id("brand_id").click()
		self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[1]/div[1]/select/option[3]').click()

		self.driver.find_element_by_id("model_id").click()
		if model == "C8":
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[2]/div[1]/select/option[3]').click()
		elif model == "C10":
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[2]/div[1]/select/option[7]').click()
		elif model == "CPE02":
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[2]/div[1]/select/option[8]').click()
		self.driver.find_element_by_id("name").send_keys(versions)
		time.sleep(2)


		#  选择语言
		self.driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/div/form/div[8]/div/input").click()
		self.driver.find_element_by_name("en-gb").click()
		if "KHM" in versions:
			Language = "ខ្មែរ"
			self.driver.find_element_by_id("searchText").click()
			pyperclip.copy(Language)
			pyautogui.hotkey('ctrl', 'v')
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[2]/div[2]/button').click()
			self.driver.find_element_by_name("km-kh").click()
		else :
			self.driver.find_element_by_name("es-es").click()
		self.driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/button[1]").click()


		pop = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[3]/div[2]/label').text
		if pop:
			print versions+"版本号已存在"
			time.sleep(1)
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/ul/li[2]/a').click()
			return False
		else:
			# 将界面拉到最底部
			js = "var q=document.documentElement.scrollTop=100000"
			self.driver.execute_script(js)
			time.sleep(3)
			# 点击保存
			self.driver.find_element_by_xpath('//*[@id="form"]/div[12]/div/button').click()
			self.driver.implicitly_wait(60)  # 隐性等待，最长等30秒
			print versions+"新建版本成功"
			get_versions = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[3]').text
			if versions == get_versions:
				self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[7]/div/a[3]').click()
				return True


	

	def add_difference_package(self,start_versions, update_version):
		# 进入添加差分包管理
		self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div[1]/div/div[1]/a").click()

		self.driver.find_element_by_class_name("select2-arrow").click()
		self.driver.find_element_by_class_name("select2-input").send_keys(start_versions)
		self.driver.find_element_by_xpath('/html/body/div[3]/ul/li/div/span').click()

		# 选项仅WIFI
		self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[4]/div/label[2]/span').click()
		self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/form/div[9]/div/div/div[2]/div[1]/div[2]/label').click()

		ota_path = update_version
		time.sleep(2)
		pyperclip.copy(ota_path)
		pyautogui.hotkey('ctrl', 'v')

		time.sleep(2)
		pyautogui.press('enter')
		time.sleep(5)

		# 将界面拉到最底部
		js = "var q=document.documentElement.scrollTop=100000"
		self.driver.execute_script(js)
		time.sleep(2)

		# 添加语言
		self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/form/div[10]/div/input').click()

		self.driver.find_element_by_name("en-gb").click()
		if "KHM" in update_version:
			Language = "ខ្មែរ"
			self.driver.find_element_by_id("searchText").click()
			pyperclip.copy(Language)
			pyautogui.hotkey('ctrl', 'v')
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[2]/div[2]/button').click()
			self.driver.find_element_by_name("km-kh").click()
		else:
			self.driver.find_element_by_name("es-es").click()
		self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/button[1]').click()
		time.sleep(2)

		# 选择分组
		if  "C8" in update_version:
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[13]/div/label[3]/span').click()
		elif "C10" in update_version:
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[13]/div/label[6]/span').click()
		elif "CPE02" in update_version:
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[13]/div/label[7]/span').click()


		while True:
			up = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/form/div[9]/div/div/div[1]/div/p[4]').text
			if up == "上传成功":
				# 点击保存
				self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/form/div[16]/div/button').click()
				time.sleep(1)
				break
			else:
				time.sleep(3)
		try:
			self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[6]/div/a').click()
		except BaseException as e:
			self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr/td[6]/div/a').click()


	def unpublish(self,model,version,last_version,last_version_number):
		# model:  型号,如 C8、C10 、CPE02
		# version: 版本号，如 1.1.2
		# last_version: 版本号的上一个版本，如1.1.0
		# last_version_number：版本号的上一个版本，如C10_KHM_v1.1.0_201810271619_user
		# 更改之前版本的差本包发布状态，若为已发布状态则取消发布，否则不做处理
		sta = 0
		if last_version_number != None:
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[1]/div/form/div/div[6]/div/input').send_keys(last_version_number)
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[1]/div/form/div/div[6]/div/span/button').click()
			status,status_number = self.get_version_status()
			if status and status_number>0:
				sta = 1
				self.click_cancel(status_number)
			else:
				print "关键字搜索没有搜索到该版本号："+last_version_number
				self.open_channel_manage()
			
		if sta == 0:
			pages = self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/div/a[9]').text
			#print pages
			end = ""
			number = ""
			status_number = 0
			clk = 1
			for page in range(int(pages)-1):
				#print page
				for i in range(1,21):
					try:
						get_version = self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[3]').text
						if model in get_version and last_version in get_version:
							i = '['+str(i)+']'
							number = i
							status,status_number = self.get_version_status(i)
							if status:
								end = "pass"
								break
						if i == 10:
							# 将界面拉到最底部
							js = "var q=document.documentElement.scrollTop=100000"
							self.driver.execute_script(js)
							time.sleep(3)
					except BaseException:
						end = "fail"
						print "最后一页，页面数量不足20，查询结束，自动退出查询"
						break
				if end != "":
					break
				else:
					try :
						if clk == 1:
							self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/div/a[10]').click()
						else:
							self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/div/a[8]').click()
					except BaseException:
						self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/div/a[8]').click()
						clk = 2
					time.sleep(1)
					#print "点击下一页"
			if end == "pass" and status_number>0:
				self.click_cancel(status_number,number)
			else:
				print model+" "+version+"版本，上个版本:"+last_version+"没有发布过差分包版本，不作处理"
			js="var q=document.documentElement.scrollTop=0"
			self.driver.execute_script(js)

		time.sleep(2)

	def released(self,version_name):
		# version_name ：发布版本号 如 C8_KHM_v2.1.4_20181120_user
		self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[1]/div/form/div/div[6]/div/input').send_keys(version_name)
		self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[1]/div/form/div/div[6]/div/span/button').click()
		sta = 0
		try:
			self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr/td[7]/div/a[3]').click()
			sta = 1
		except BaseException as e:
			print version_name+"版本不存在"
		if sta == 1:
			index = ""
			try:
				self.driver.find_element_by_xpath('//html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr[2]/td[4]/span').text
				index = "1"
			except BaseException as e:
				self.click_released(index)
			if index != "":
				try:
					for i in range(1,21):
						index = "["+str(i)+"]"
						self.click_released(index)
				except BaseException:
					#print index
					pass
			return True
		else:
			return False

	def click_released(self,index):
		# 根据index的行，保持该行的差分包状态为保持到发布状态
		for i in range(6):
			stats = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr'+index+'/td[4]/span').text
			if stats == "待测试" or stats == "已下线":
				self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr'+index+'/td[6]/div/a').click()
			elif stats == "已发布":
				break
			else:
				self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr'+index+'/td[6]/div/a[1]').click()

	def get_version_status(self, i=""):
		# 根据index的行，获取固件管理界面，版本状态 的发布状态数据
		status_number = 0
		try:
			status = self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr'+i+'/td[6]').text
			a = unicode('已发布', 'utf-8')
			if a in status:
				status = status.encode('gb18030')
				status = str(re.findall(r"\(\d{1,3}\)",status))
				status_number = int(status.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", ''))
				return True,status_number
			else:
				print "查到到对应的版本，但未发布过差分包版本"
				return True,status_number
		except BaseException:
			return False, status_number

	def click_cancel(self,status_number,number=""):
		# status_number 为已发布版本的数量
		# number 操作的列
		self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr'+number+'/td[7]/div/a[3]').click()
		if status_number == 1:
			in_status = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr/td[4]/span').text
			if in_status =="已发布":
				print "版本为已发布状态，点击取消发布"
				self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr/td[6]/div/a').click()
				in_status = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr/td[4]/span').text
				time.sleep(2)
				if in_status != "已发布":
					print "旧版本取消差分包发布成功"
		else:
			for i in range(1,status_number+1):
				in_status = self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/span').text
				if in_status =="已发布":
					print "版本为已发布状态，点击取消发布"
					self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[6]/div/a').click()
					in_status = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/span').text
					time.sleep(2)
					if in_status != "已发布":
						print "旧版本取消差分包发布成功"

	def quit(self):
		self.driver.quit()

	def start(self,model,version_name):
		self.open_channel_manage()
		end = self.add_firmware(version_name, model)
		return end
