#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Send_Mail:
	def start(self,msg):
		# 发件人
		from_addr = "liqingxia@cootf.com"
		password  = "tq04v8t923_JB"
		smtp_server = 'smtp.mxhichina.com'

		# 接收人
		to_addr  = ["121261667@qq.com"]
		# 抄送人
		cc = ["121261667@qq.com","liqingxia3344@126.com"]

		# 接收人
		#to_addr  = ["ctfcs@cootf.com"]
		# 抄送人
		#cc = ["zhangyupeng@cootf.com","yuanfuchao@cootf.com","yuanfuchao@cootf.com","xinziwei@cootf.com","wanghui@cootf.com","liangzhongwei@cootf.com","mayingying@cootf.com","hanshuming@cootf.com"]


		toaddrs = to_addr + cc

		# 邮件内容
		message ="以下版本编译完成，请进行测试：\n"
		for i in msg:
			message = message + i + "\n"

		msg = MIMEText(message,'plain','utf-8')

		# 邮件主题
		msg['Subject'] = Header('OTA差分包上传完成，申请测试','utf-8')
		# 显示发件人
		msg['From'] = Header('liqingxia@cootf.com')
		# 显示收件人
		msg['To'] = Header('ctfcs@cootf.com','utf-8')
		# 显示抄送
		msg['Cc'] = Header('"zhangyupeng@cootf.com","yuanfuchao@cootf.com","yuanfuchao@cootf.com","xinziwei@cootf.com","wanghui@cootf.com","liangzhongwei@cootf.com","mayingying@cootf.com","hanshuming@cootf.com"',"utf-8")

		try:
			server = smtplib.SMTP(smtp_server,25) #第二个参数为默认端口为25，有些邮件有特殊端口
			print('开始登录Email')
			server.login(from_addr,password) #登录邮箱
			print('登录成功')
			print("邮件开始发送")
			server.sendmail(from_addr,toaddrs,msg.as_string())  #将msg转化成string发出
			server.quit()
			print("邮件发送成功")
		except smtplib.SMTPException as e:
			print("邮件发送失败",e)

 
