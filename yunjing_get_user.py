import json
import os
import random
import smtplib
import time
import requests
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime


def send_email(recv_email,info_title, website_url):
    # 可以使用其他邮箱，支持smtp即可
    # smtp host
    mail_host = 'smtp.163.com'
    # send email user
    mail_user = 'xxxxxxxx@163.com'
    # smtp pass
    mail_pass = 'xxxxxxxxxxxxxxxx'
    # 发送者邮箱
    sender = 'xxxxxxx@163.com'
    # 接收者邮箱
    receivers = [recv_email]
    message_information = website_url
    message = MIMEText(message_information, 'plain', 'utf-8')
    message['Subject'] = info_title
    message['From'] = sender
    message['To'] = receivers[0]
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print('Send ' + message_information + ' success.')
    except smtplib.SMTPException as e:
        print('error', e)


def user_info_delete_repeat(read_file_name):
    if os.path.exists(f"{read_file_name}.csv"):
        temp=pd.read_csv(f"{read_file_name}_temp.csv",encoding="utf-8",header=None)
        data=pd.read_csv(f"{read_file_name}.csv",encoding="utf-8",header=None).append(temp)
    else:
        data=pd.read_csv(f"{read_file_name}_temp.csv",encoding="utf-8",header=None)
    data = data.drop_duplicates()
    data.to_csv(f"{read_file_name}.csv", index=False,header=0)


def website_render(recv_email, yunjing_data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'SIGN': yunjing_data['SIGN'],
        'Origin': 'https://yunjing.ichunqiu.com',
        'Connection': 'keep-alive',
        'Referer': 'https://yunjing.ichunqiu.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=1'
    }

    result = requests.post('https://apicloud.ichunqiu.com/student/user/sign_in', headers=headers,
                           data=yunjing_data['raw_data'])

    user_info=requests.post('https://apicloud.ichunqiu.com/student/member/detail', headers=headers,
                           data=yunjing_data['raw_data'])
    user_info_json=json.loads(user_info.content)

    # {"code":100,"message":"参数不合法"}
    # {"code":0,"message":"打卡成功","reward_grit":0}
    # {"code":114,"message":"token已经失效"}
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    open("yunjing.log.txt", "a").write(f"[{current_time}] {yunjing_data['SIGN']} {result.text}\n")

    if "token已经失效" not in user_info.text:
        info=pd.DataFrame({
            "SIGN":yunjing_data['SIGN'],
            "user_name":user_info_json['data']['user_name'],
            "phone":user_info_json['data']['phone'],
            "is_bind_wx":'是' if user_info_json.get('data', {}).get('is_bind_wx') == 1 else '否',
            "wx_nickname": user_info_json['data']['wx_nickname']
        }, index=[0])
        info.to_csv("user_info_temp.csv", index=False, mode="a")

    if "token已经失效" in result.text:
        title_prefix = "[春秋云镜]"
        title_info = "token已经失效"
        title = title_prefix + " " + title_info
        # 获取ip功能存在问题
        # server_ip=os.popen("curl ifconfig.me").read()
        try:
            user_detail=pd.read_csv(f"user_info.csv",encoding="utf-8")
            # 通过SIGN匹配获取对应用户信息
            user_sign_info = user_detail[user_detail['SIGN'] == yunjing_data['SIGN']].iloc[0]

            info = (
                f"IP为：【自行填写】机器上的春秋云镜自动打卡功能打卡失败，请访问 https://yunjing.ichunqiu.com/login 重新登录获取信息\n"
                f"\n用户信息："
                f"\n平台用户名：{user_sign_info['user_name']}"
                f"\n用户电话：{user_sign_info['phone']}"
                f"\n是否绑定微信：{user_sign_info['is_bind_wx']}"
                f"\n微信用户名：{user_sign_info['wx_nickname']}\n"
                f"\nSIGN：{yunjing_data['SIGN']}"
                f"\nraw_data：{yunjing_data['raw_data']}"
                f"\n\n返回值：{result.text}")
        except:
            info = (
                f"IP为：【自行填写】机器上的春秋云镜自动打卡功能打卡失败，请访问 https://yunjing.ichunqiu.com/login 重新登录获取信息\n"
                f"\n用户信息获取失败，此token未获取过信息\n"
                f"\nSIGN：{yunjing_data['SIGN']}"
                f"\nraw_data：{yunjing_data['raw_data']}"
                f"\n\n返回值：{result.text}")
        send_email(recv_email, title, info)
    else:
        print(result.text)


if __name__ == "__main__":
    data=pd.read_csv("yunjing_data.csv",encoding="utf-8",sep=' ',header=0)
    for i in range(len(data)):
        recv_email_i=data.loc[i, "recv_email"]
        yunjing_data = {
            'SIGN': data.loc[i, "SIGN"],
            'raw_data': data.loc[i, "raw_data"]
        }
        website_render(recv_email_i,yunjing_data)
        time.sleep(random.randint(1,6))
    user_info_delete_repeat("user_info")
