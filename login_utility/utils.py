import tempfile

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404


class SendEmail(object):

    def __init__(self, request=None, headers=None, sender=None, backend=None , file=[]):
        self.request = request
        self.headers = headers
        self.from_name = settings.DEFAULT_FROM_EMAIL_NAME
        self.file = file

        if sender:
            self.sender = sender
        else:
            self.sender = settings.DEFAULT_FROM_EMAIL

    def send_by_template(self, recipient, template_path, context, subject, bcc_email=[], cc_email=[]):
        """
        send email function with template_path. will do both rendering & send in this function.
        should not change the interface.
        """
        body = self.email_render(template_path, context)
        self.send_email(recipient, subject, body, bcc_email, cc_email)

    def send_by_body(self, recipient, subject, body, bcc_email=[], cc_email=[]):
        """
        send email function with text. will do both rendering & send in this function.
        should not change the interface.
        """
        try:
            self.send_email(recipient, subject, body, bcc_email, cc_email)
        except Exception:
            pass

    def send_email(self, recipient, subject, body, bcc_email, cc_email):
        """
        send email with rendered subject and body
        """
        msg = EmailMultiAlternatives(subject, subject, self.sender, recipient, bcc=bcc_email, cc=cc_email)

        msg.attach_alternative(body, "text/html")

        if self.file:
            for file in self.file:
                basename = file.name.split('.')[0]
                extension = '.' + file.name.split('.')[1]
                tmp_file = tempfile.NamedTemporaryFile(mode='wb', prefix=basename, suffix=extension)
                tmp_file.write(file.read())
                tmp_file.flush()
                msg.attach_file(tmp_file.name)

        msg.send()

    def email_render(self, template_path, context):
        """
        wrapper to generate email subject and body
        """
        if self.request is None:
            body = render_to_string(template_path, context)
        else:
            body = render_to_string(template_path, context, RequestContext(self.request))
        return body
