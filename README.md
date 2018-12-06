基于python 2版本，调用shell脚本生成差分包；生成完成自动上传到WEB后台、自动发布与取消上一版发布状态

在目录/home/build/test/ota_build/下运行脚本
该脚本支持C8、C10、CPE02；运行python脚本时需要手动输入验证码（输入验证码时间等待60秒，不需要点击登录）



# 运行自动编译差分包并上传到后台，状态会变为测试中
python build_package.py

# 发布最新上传的版本，并取消上一版本的发布状态 
python released.py 




# 存放原始文件目录为，以C8为例： /home/build/MK_OTA/C8/C8_ota_package
# 生成的差分包路径，以C8为例： /home/build/MK_OTA/out/C8
# 差分包命名规则，以C8，17-21版本为例：C8_update1.1.17-1.1.21.zip
