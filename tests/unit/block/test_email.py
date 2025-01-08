from email.message import Message
from unittest.mock import MagicMock, call, patch, sentinel

import yaml

import pybloqs

user_config = yaml.full_load(
    """
        smtp_kwargs:
          host: smtp.example.com
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
          user: lovelace@example.com
          password: my_password
        tmp_html_dir: /tmp
        user_email_address: lovelace@example.com"""
)


def test_send():
    message = Message()
    recipients = ["bayes@example.com", "cantor@example.com"]
    message["From"] = ["lovelace@example.com"]
    message["To"] = recipients
    message.as_string = MagicMock(return_value=sentinel.message_string)
    m_SMTP = MagicMock()

    with patch("pybloqs.email.smtplib") as m_smtplib:
        m_smtplib.SMTP = m_SMTP
        with patch("pybloqs.email.user_config", user_config):
            pybloqs.email.send(message, recipients)

    ex_calls = [
        call(host="smtp.example.com", port=587),
        call().ehlo(),
        call().starttls(),
        call().ehlo(),
        call().login(password="my_password", user="lovelace@example.com"),
        call().sendmail(["lovelace@example.com"], ["bayes@example.com", "cantor@example.com"], sentinel.message_string),
        call().quit(),
    ]

    assert ex_calls == m_SMTP.mock_calls
