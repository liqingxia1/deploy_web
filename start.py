# -*- coding: utf-8 -*-
from build_package import *
from released import *


if __name__ == "__main__":
    opt = input('''请输入要执行的操作
            1. 生成查分包并上传到web
            2. 更新最新版本差分包状态，取消上一版本差分包发布状态
            3. 生成差分包上传到web，并取消上一版差分包发布状态，将最新版本设为发布状态
        	''')


    if opt>0 and opt <4:
        identifiers = {}
        identifier = input('''请输入编号，选择要操作的型号
            1. CPE02
            2. C8_NCA
            3. C8_KHM
            4. C10_NCA
            5. C10_KHM
            ''')

        identifiers[1] = "CPE02"
        identifiers[2] = "C8_NCA"
        identifiers[3] = "C8_KHM"
        identifiers[4] = "C10_NCA"
        identifiers[5] = "C10_KHM"
        if opt == 1:
            build_run(identifiers[identifier])
        elif opt == 2:
            released_run(identifiers[identifier])
        elif opt == 3:
            web_opt = build_run(identifiers[identifier])
            released2_run(identifiers[identifier], web_opt)
    else:
        print "输入异常，程序结束"

