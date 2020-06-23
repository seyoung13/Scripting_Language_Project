# -*- coding: cp949 -*-
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.base64mime import body_encode as encode_base64


class MySMTP(smtplib.SMTP):

    def login(self, user, password):
        def encode_cram_md5(challenge, user, password):
            challenge = base64.decodestring(challenge)
            response = user + " " + hmac.HMAC(password, challenge).hexdigest()
            return encode_base64(response)

        def encode_plain(user, password):
            s = "\0%s\0%s" % (user, password)
            return encode_base64(s.encode('ascii'), eol='')

        AUTH_PLAIN = "PLAIN"
        AUTH_CRAM_MD5 = "CRAM-MD5"
        AUTH_LOGIN = "LOGIN"

        self.ehlo_or_helo_if_needed()

        if not self.has_extn("auth"):
            raise smtplib.SMTPException("SMTP AUTH extension not supported by server.")

        authlist = self.esmtp_features["auth"].split()
        preferred_auths = [AUTH_CRAM_MD5, AUTH_PLAIN, AUTH_LOGIN]

        authmethod = None
        for method in preferred_auths:
            if method in authlist:
                authmethod = method
                break

        if authmethod == AUTH_LOGIN:
            code, resp = self.docmd("AUTH",
                                      "%s %s" % (AUTH_LOGIN, encode_base64(user)))
            if code != 334:
                raise smtplib.SMTPAuthenticationError(code, resp)
            (code, resp) = self.docmd(encode_base64(password))
        elif authmethod == AUTH_PLAIN:
            temp_encode_plain = str(encode_plain(user, password))
            temp_encode_plain = temp_encode_plain.replace("\n", "")
            (code, resp) = self.docmd("AUTH",
                                      AUTH_PLAIN + " " + temp_encode_plain)
        elif authmethod == AUTH_CRAM_MD5:
            (code, resp) = self.docmd("AUTH", AUTH_CRAM_MD5)
            if code == 503:
                return code, resp
            (code, resp) = self.docmd(encode_cram_md5(resp, user, password))
        elif authmethod is None:
            raise smtplib.SMTPException("No suitable authentication method found.")
        if code not in (235, 503):
            raise smtplib.SMTPAuthenticationError(code, resp)
        return code, resp


def send_email(message, target_address):
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"

    sender_address = "skview1201@gmail.com"     # 보내는 사람 email 주소.
    recipient_address = target_address  # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = '대중교통 환승 경로 정보'
    msg['From'] = sender_address
    msg['To'] = recipient_address

    message = MIMEText(message)
    msg.attach(message)

    # 메일을 발송한다.
    s = MySMTP(host, port)
    # s.set_debuglevel(1) # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("skview1201@gmail.com", "tmzk)#0106")
    s.sendmail(sender_address, [recipient_address], msg.as_string())
    s.close()
