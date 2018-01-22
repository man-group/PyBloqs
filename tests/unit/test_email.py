from mock import patch, MagicMock, sentinel, call
import yaml
from email.message import Message
from pybloqs.email import send

user_config = \
    yaml.load(
        """
        smtp_kwargs:
          host: smtp.gmail.com
          port: 587
        smtp_pre_login_calls:
        - !!python/tuple
          - ehlo
          - {}
        - !!python/tuple
          - starttls
          - {}
        - !!python/tuple
          - ehlo
          - {}
        smtp_login:
          user: djepson@gmail.com
          password: my_password
        tmp_html_dir: /tmp
        user_email_address: me@gmail.com""")


def test_send():
    message = Message()
    recipients = ['me@gmail.com', 'me@ahl.com']
    message['From'] = ['origin@gmail.com']
    message['To'] = recipients
    message.as_string = MagicMock(return_value=sentinel.message_string)
    m_SMTP = MagicMock()

    with patch('pybloqs.email.smtplib') as m_smtplib:
        m_smtplib.SMTP = m_SMTP
        with patch('pybloqs.email.user_config', user_config):
            send(message, recipients)

    ex_calls = [
        call(host='smtp.gmail.com', port=587),
        call().ehlo(),
        call().starttls(),
        call().ehlo(),
        call().login(password='my_password', user='djepson@gmail.com'),
        call().sendmail(['origin@gmail.com'], ['me@gmail.com', 'me@ahl.com'], sentinel.message_string),
        call().quit()]

    assert ex_calls == m_SMTP.mock_calls
