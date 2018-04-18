from random import Random # 用于生成随机码 
from django.core.mail import send_mail # 发送邮件模块
from jwt_auth.models import EmailVerifycode # 邮箱验证model
from TripitakaPlatform.settings import EMAIL_FROM  # setting.py添加的的配置信息

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_verifycode_email(email, send_type):
    EmailVerifycode.objects.filter(email=email).delete()
    email_record = EmailVerifycode()
    # 将给用户发的信息保存在数据库中
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "找回您的密码"
        email_body = "龙泉大藏经校勘平台用户您好，\n您已发起用户重置密码请求，您的本次操作验证码为：{0}。如果不是您本人操作，请忽略此邮件！\n阿弥陀佛！".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print('send_status',send_status,email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
        return send_status
