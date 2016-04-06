from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    error_messages = {
        "email_not_exists": _("This email id does not exists.Enter a Valid email-id."),
    }
    email = forms.EmailField(max_length=75)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email", "")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["email_not_exists"], code="email_not_exists",)
        else:
            user = User.objects.get(email=email)
            cleaned_data["username"] = user.username
        return cleaned_data

class EmailVerifyForm(forms.Form):

    error_messages = {
        "email_not_exists": _("This email id does not exists"),
    }
    email = forms.EmailField(max_length=75)

    def clean(self):
        cleaned_data = super(EmailVerifyForm, self).clean()
        email = cleaned_data.get("email", "")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["email_not_exists"], code="email_not_exists",)
        return cleaned_data

class ResetPasswordForm(forms.Form):
    error_messages = {
        "password_match": _("Password did not match."),
    }
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        new_password = cleaned_data.get("new_password", "")
        confirm_password = cleaned_data.get("confirm_password", "")
        if new_password != confirm_password:
            raise forms.ValidationError(self.error_messages["password_match"], code="password_match",)
        return cleaned_data
