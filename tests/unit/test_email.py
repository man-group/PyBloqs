# This Python file uses the following encoding: utf-8
from mock import patch, MagicMock, sentinel, call, ANY
import yaml
from email.message import Message

import pybloqs


user_config = \
    yaml.load(
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
        user_email_address: lovelace@example.com""")


def test_send():
    message = Message()
    recipients = ['bayes@example.com', 'cantor@example.com']
    message['From'] = ['lovelace@example.com']
    message['To'] = recipients
    message.as_string = MagicMock(return_value=sentinel.message_string)
    m_SMTP = MagicMock()

    with patch('pybloqs.email.smtplib') as m_smtplib:
        m_smtplib.SMTP = m_SMTP
        with patch('pybloqs.email.user_config', user_config):
            pybloqs.email.send(message, recipients)

    ex_calls = [
        call(host='smtp.example.com', port=587),
        call().ehlo(),
        call().starttls(),
        call().ehlo(),
        call().login(password='my_password', user='lovelace@example.com'),
        call().sendmail(['lovelace@example.com'], ['bayes@example.com', 'cantor@example.com'], sentinel.message_string),
        call().quit()]

    assert ex_calls == m_SMTP.mock_calls


def test_send_html_report_utf8():
    with patch('pybloqs.email.smtplib.SMTP') as mock_smtp_constructor, \
            patch('pybloqs.email.user_config', user_config):
        bloq = pybloqs.VStack([pybloqs.Block(u"This should show euro '€'.")])
        bloq.email(title='Test bloqs email: utf-8',
                   from_address='lovelace@example.com',
                   recipients=['bayes@example.com', 'cantor@example.com'],
                   cc=['fourier@example.com', 'galois@example.com'],
                   bcc=['hilbert@example.com', 'ito@example.com'],
                   convert_to_ascii=False)

    mock_smtp_constructor.return_value.sendmail.assert_called_once_with('lovelace@example.com', ['bayes@example.com', 'cantor@example.com', 'fourier@example.com',
                                                                                             'galois@example.com', 'hilbert@example.com', 'ito@example.com'],  ANY)
    msg = mock_smtp_constructor.return_value.sendmail.call_args[0][2]
    assert 'Subject: Test bloqs email: utf-8' in msg
    assert 'From: lovelace@example.com' in msg
    assert 'To: bayes@example.com,cantor@example.com' in msg
    assert 'Cc: fourier@example.com,galois@example.com' in msg
    assert 'hilbert@example.com' not in msg and 'ito@example.com' not in msg
    assert 'Content-Type: text/html; charset="utf-8"' in msg


def test_send_html_report_ascii():
    with patch('pybloqs.email.smtplib.SMTP') as mock_smtp_constructor, \
            patch('pybloqs.email.user_config', user_config):
        bloq = pybloqs.VStack([pybloqs.Block(u"This should show euro '€'.")])
        bloq.email(title='Test bloqs email: ascii', from_address='lovelace@example.com', recipients=['bayes@example.com'])

    mock_smtp_constructor.return_value.sendmail.assert_called_once_with('lovelace@example.com', ['bayes@example.com'],  ANY)
    msg = mock_smtp_constructor.return_value.sendmail.call_args[0][2]
    assert 'Subject: Test bloqs email: ascii' in msg
    assert 'From: lovelace@example.com' in msg
    assert 'To: bayes@example.com' in msg
    assert 'Content-Type: text/html; charset="us-ascii"' in msg
    assert "This should show euro ''." in msg   # this has stripped out the non ascii / utf8 char
