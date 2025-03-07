# 春秋云镜打卡
需要自行添加信息并设置发送接受邮箱，详见下文\
\
yunjing.py\
不会获取用户信息并在邮件中添加用户信息\
\
yunjing_get_user.py\
会获取用户信息并在邮件中添加，同时会在本地创建csv文件保存此信息

## 2025.3.8更新
yunjing.py写入log时增加时间和SIGN\
yunjing_get_user.py写入log时增加时间

## SIGN & raw_data获取方式
![image](https://github.com/user-attachments/assets/55c0ec8a-2bd6-4555-93a9-022d727e50e3)
![image](https://github.com/user-attachments/assets/d22b5315-8a32-4b0c-811c-8203c44caa5c)

## 要修改的内容
![image](https://github.com/user-attachments/assets/27b34c99-8f43-4a23-92e3-17c11138bb31)\
以及yunjing_data.csv中的值（使用空格分隔）
recv_email SIGN raw_data
接收者邮箱 获取的SIGN 获取的data

## 效果预览
![image](https://github.com/user-attachments/assets/be1a495c-ae4c-4c19-be21-b73333017327)
![image](https://github.com/user-attachments/assets/810661e9-fe68-48c4-8149-b1cce9d0ad1c)
