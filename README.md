在目录/home/build/test/ota_build/下运行脚本
该脚本支持C8、C10、CPE02；运行python脚本时需要手动输入验证码（输入验证码时间等待60秒，不需要点击登录）



# 运行脚本,根据提示输入对应编号执行对于的操作
python start.py



# 存放原始文件目录为，以C8_KHM为例： /home/build/MK_OTA/C8/C8_ota_package/KHM
# 生成的差分包路径，以C8_KHM 2.1.12版本为例： /home/build/MK_OTA/Dif_packet/C8_KHM/2.1.12/
# 差分包命名规则，以C8_KHM，10-12版本为例： C8_KHM_update2.1.10-2.1.12.zip
