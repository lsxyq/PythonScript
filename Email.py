#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:Leslie-x 

import smtplib, time, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders


class Settings():
    def __init__(self, username, password, subject, server, sender, receiver):
        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.username = username
        self.password = password
        self.subject = subject
        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        # subject = '中文标题'
        # subject=Header(subject, 'utf-8').encode()


class Message():
    # 构造邮件对象MIMEMultipart对象
    _msg = MIMEMultipart('mixed')

    def __init__(self, set, content):
        # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        self._msg['Subject'] = set.subject
        self._msg['From'] = set.username
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        self._msg['To'] = ";".join(set.receiver)
        self._msg['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.content = content

    def get_msg(self):
        for info in self.content.get_content():
            if not info: continue
            self._msg.attach(info)
        return self._msg


class EmailContent():
    def __init__(self, text=None, html=None, image_path=None, att_path=None):
        self.text = text
        self.image = image_path
        self.html = html
        self.att_path = att_path

    def get_filename(self, path):
        import os
        return os.path.basename(path)

    @property
    def get_text(self):
        # 构造文本
        if not self.text:
            return None
        self.text_plain = MIMEText(self.text, 'plain', 'utf-8')
        return self.text_plain

    @property
    def get_image(self):
        # 构造图片链接
        if not self.image:
            return None
        if not os.path.exists(self.image):
            raise FileNotFoundError("Not Find This File")
        filename = self.get_filename(self.image)
        self.sendimagefile = open(r'%s' % self.image, 'rb').read()
        self.image = MIMEImage(self.sendimagefile)
        self.image.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
        return self.image

    @property
    def get_html(self):
        # 构造html
        if not self.html:
            return None
        self.text_html = MIMEText(self.html, 'html', 'utf-8')
        self.text_html["Content-Disposition"] = 'attachment; filename="TEXT/HTML.html"'
        return self.text_html

    @property
    def get_att(self):
        "# 构造附件"
        if not self.att_path:
            return None
        if not os.path.exists(self.att_path):
            raise FileNotFoundError("Not Find This File")
        filename = self.get_filename(self.att_path)
        self.att = MIMEBase('application', 'octet-stream')
        self.att.set_payload(open(self.att_path, 'rb').read())
        self.att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
        encoders.encode_base64(self.att)
        return self.att

    def get_content(self):
        return self.get_text, self.get_image, self.get_html, self.get_att


class Smtp():
    _smtp = smtplib.SMTP()

    def __init__(self, set, msg):
        self.set = set
        self.msg = msg

    def _connect(self):
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        self._smtp.connect(self.set.server)

    def _login(self):
        self._smtp.login(self.set.username, self.set.password)

    def _sendmail(self):
        self._smtp.sendmail(self.set.sender, self.set.receiver, self.msg.as_string())

    def _quit(self):
        self._smtp.quit()

    def start(self):
        self._connect()
        self._login()
        self._sendmail()
        self._quit()


"""
可选参数
text 邮件正文内容（文本）
html 邮件附件内容（HTML）
image_path 邮件附件内容（图片路径）
att_path 邮件附件内容（文件路径）
"""
text = "Hi!你好啊！！\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com"
html = """
<html>  
  <head></head>  
  <body>  
    <p>Hi!<br>  
       How are you?<br>  
       Here is the <a href="http://www.baidu.com">link</a> you wanted.<br> 
    </p> 
  </body>  
</html>  
"""
image_path = "F:\爬虫\IMGS\高桥圣子1.jpg"
att_path = r'F:\Python开发工程师测试题（一）.docx'

"""
必要参数
username  邮箱登陆账号
password  邮箱密码
subject   邮件主题
server    邮件服务器
sender    发送方
receiver  收件人（列表格式，多个收件人）
"""
username = "18358467482@139.com"
password = '359287416q'
subject = '测试邮件'
server = 'smtp.139.com'
sender = '18358467482@139.com'
receiver = ['454922491@qq.com']

if __name__ == '__main__':
    set = Settings(username, password, subject, server, sender, receiver)
    content = EmailContent(text=text, image_path=image_path, att_path=att_path, html=html)
    message = Message(set, content)
    msg = message.get_msg()
    smtp = Smtp(set, msg)
    smtp.start()
