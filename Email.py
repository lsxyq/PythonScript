#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author:Leslie-x
import smtplib, time, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders


class Message():
    # 构造邮件对象MIMEMultipart对象
    _msg = MIMEMultipart('mixed')

    def __init__(self):
        pass

    @classmethod
    def get_text(cls, text):
        """
        :param text:
            eg :Hello！\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com
        :return:
        """
        if not text:
            return None
        text_plain = MIMEText(text, 'plain', 'utf-8')
        return text_plain

    @classmethod
    def get_image(cls, image_path):
        """
        :param image_path:
            eg: F:\a\b\c.jpg
        :return:
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError("Not Find This File")
        filename = os.path.basename(image_path)
        image_data = open(r'%s' % image_path, 'rb').read()
        image = MIMEImage(image_data)
        image.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
        return image

    @classmethod
    def get_html(cls, html):
        """
        :param html:
            <html>
              <head></head>
              <body>
                <p>Hi!<br>
                   How are you?<br>
                   Here is the <a href="http://www.baidu.com">link</a> you wanted.<br>
                </p>
              </body>
            </html>
        :return:
        """
        if not html:
            return None
        text_html = MIMEText(html, 'html', 'utf-8')
        text_html["Content-Disposition"] = 'attachment; filename="TEXT/HTML.html"'
        return text_html

    @classmethod
    def get_att(cls, att_path):
        """
        :param att_path:
            eg:F:\Python开发工程师测试题（一）.docx
        :return:
        """
        if not os.path.exists(att_path):
            raise FileNotFoundError("Not Find This File")
        filename = os.path.basename(att_path)
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(open(att_path, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
        encoders.encode_base64(att)
        return att

    def get_msg(self, text=None, html=None, image_path=None, att_path=None):
        info_list = []
        info_list.append(Message.get_text(text))
        info_list.append(Message.get_html(html))
        info_list.append(Message.get_att(att_path))
        info_list.append(Message.get_image(image_path))
        for info in info_list:
            if not info: continue
            self._msg.attach(info)
        return self._msg


class SmtpServer():
    _smtp = smtplib.SMTP()

    def __init__(self, config):
        self.config = config

    def __getattr__(self, item):
        value = self.config.get(item, None)
        if not value:
            raise AttributeError("object has no attribute '%s'" % item)
        return value

    def message_set(self, msg):
        """
        下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        subject = '中文标题'
        subject=Header(subject, 'utf-8').encode()
        收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        """
        msg['From'] = self.username
        msg['Subject'] = self.subject
        msg['To'] = ";".join(self.receiver)
        msg['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return msg

    def send_email(self, msg: MIMEMultipart):
        email = self.message_set(msg)
        self._smtp.connect(self.server)
        self._smtp.login(
            user=self.username,
            password=self.password
        )
        self._smtp.sendmail(
            from_addr=self.sender,
            to_addrs=self.receiver,
            msg=email.as_string()
        )
        self._smtp.quit()


if __name__ == '__main__':
    config = {
        'username': "xxxx9.com",
        "password": "xxxx",
        "subject": '测试邮件',
        "server": "smtp.139.com",
        "sender": "xxx@139.com",
        "receiver": ['xxx@qq.com']
    }
    t = r'Hello！\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com'
    msg = Message().get_msg(text=t)
    SmtpServer(config).send_email(msg)
