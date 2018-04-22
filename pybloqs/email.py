"""
Common email related functions used by various reports.
"""
from __future__ import absolute_import

import base64
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import logging
import os
import smtplib
import tempfile

from html5lib import treebuilders
import html5lib
import six

from pybloqs.config import user_config


_log = logging.getLogger(__name__)


def send(message, recipients):
    """
    Send an email to a list of recipients.

    - If the message is missing the From address it's set to the current user [#x]_.
    - If the message is missing the To field it's set to recipients [#x]_.
    - If add_footer is True and message is a subclass of MIMEBase the standard
      report email footer will be added before the email's sent.

    :param message: email.message.Message or subclass, eg email.mime.MIMEMultpart
    :param recipients: list of email addresses

    .. [#x] the original message is modified in these cases.
    """
    assert isinstance(message, Message)
    assert isinstance(recipients, (list, tuple))

    if not message["From"]:
        message["From"] = getpass.getuser()

    if not message["To"]:
        message["To"] = ",".join(recipients)

    s = smtplib.SMTP(**user_config["smtp_kwargs"])
    if 'smtp_pre_login_calls' in user_config:
        smtp_pre_login_calls = user_config['smtp_pre_login_calls']
        for method, kwargs in smtp_pre_login_calls:
            getattr(s, method)(**kwargs)
    if 'smtp_login' in user_config:
        s.login(**user_config['smtp_login'])
    s.sendmail(message["From"], recipients, message.as_string())
    s.quit()


def _set_email_mime_types(dom, message=None, convert_to_ascii=False):
    """
    Takes HTML dom object and constructs email object (MIMEMultipart)
    images referenced in html <img src=c:/test.png /> are attached as MIMEImage and
    reference in html part of email are replaced to reference these attachment
    in format <img src=cid:test.png />

    Returns - MIMEMultipart object
    :param dom: dom of the html message
    :param message: MIMEMultipart object (new instance created if None)
    :param convert_to_ascii: bool convert html format to ascii
    """
    # Create MIME
    if not message:
        message = MIMEMultipart()

    idx = 0
    subtype = None

    img_mimes = []
    # replace image paths with embedded images
    for img_tag in dom.getElementsByTagName("img"):
        src = img_tag.getAttribute("src")
        # Embedded images need special treatment
        if src.startswith("data:image"):
            name = "%s_embedded" % idx

            hdr = "data:image/"
            hdr_index = src.index(hdr) + len(hdr)
            imgdef = src[hdr_index:]
            subtype = imgdef[:imgdef.index(";")]

            # At the moment outlook doesn't support SVG so remove such images.
            # TODO: Rasterize the SVG on the fly for embedding.
            if subtype.lower() == "svg+xml":
                img_tag.parentNode.removeChild(img_tag)
                continue
            img_data = base64.b64decode(imgdef[(imgdef.index("base64,") + 7):])
        else:
            # get a unique name for the image
            name = "%s_%s" % (idx, os.path.basename(src))

            with open(src, "rb") as fp:
                img_data = fp.read()

        img_mime = MIMEImage(img_data, _subtype=subtype)

        img_mime.add_header("Content-Disposition", "attachment", filename=name)
        img_mimes.append(img_mime)

        # replace the path with the embedded image
        img_tag.setAttribute("src", "cid:%s" % name)

        idx += 1

    html = dom.toxml()
    if isinstance(html, six.text_type) and convert_to_ascii:
        html = html.encode("us-ascii", "ignore")
        message.attach(MIMEText(html, "html", "us-ascii"))
    else:
        message.attach(MIMEText(html, "html", "utf-8"))

    for img_mime in img_mimes:
        message.attach(img_mime)

    return message


def send_html_report(html_str, to, subject=None, attachments=None, From=None, Cc=None, Bcc=None, convert_to_ascii=True):
    """
    Email html report and embed any images.
    Extract html title to email subject.

    :return: MIMEMultipart object
    :param html_str: html string to send in the email body
    :param to: list of recipients
    :param subject: email subject
    :param attachments: a list of tuple(extension, filename)
    :param From: from, sender of the message
    :param Cc: cc recipient
    :param Bcc: bcc recipient
    :param convert_to_ascii: bool convert html format to ascii
     """
    # create the dom for querying/modifying the html document
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    dom = parser.parse(html_str)

    if not subject:
        # try to find title string in html
        for title in dom.getElementsByTagName("title"):
            if title.childNodes:
                subject = title.childNodes[0].data
                break

    # create the message and embed any images
    mime_msg = _set_email_mime_types(dom, convert_to_ascii=convert_to_ascii)

    if subject:
        mime_msg["Subject"] = subject

    if From:
        mime_msg["From"] = From

    mime_msg["To"] = ",".join(to)

    if Cc:
        mime_msg["Cc"] = ",".join(Cc)

    # set recipients to be union of to, cc'd and bcc'd addresses
    to = sorted(set(to) | set(Cc or []) | set(Bcc or []))

    if attachments is not None:
        for attachment_spec in attachments:
            try:
                filename_no_ext = subject
                fmt, content = attachment_spec
            except ValueError:
                filename_no_ext, fmt = os.path.splitext(os.path.split(attachment_spec)[-1])
                # Exclude the dot from the extension, gosh darn it!
                fmt = fmt[1:]
                if fmt == '':
                    raise ValueError('Attachment file name has no extension:', attachment_spec)

                with open(attachment_spec, "rb") as f:
                    content = f.read()

            attachment = MIMEBase("application", fmt)
            attachment.set_payload(content)

            encoders.encode_base64(attachment)

            filename_base = filename_no_ext or os.path.basename(tempfile.mktemp())
            attachment_spec = filename_base + "." + fmt

            attachment.add_header('Content-Disposition',
                                  'attachment',
                                  filename=attachment_spec)
            mime_msg.attach(attachment)

    send(mime_msg, to)
    return mime_msg
