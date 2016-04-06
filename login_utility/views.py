from django.shortcuts import render


from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.urlresolvers import reverse

from forms import LoginForm, EmailVerifyForm, ResetPasswordForm
from utils import SendEmail
from models import PasswordResetAuth 

def login_user(request):

    if request.user.is_authenticated():
         return redirect(settings.AFTER_LOGIN_REDIRECT_URL)

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            print "form valid"
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(settings.AFTER_LOGIN_REDIRECT_URL)

            error_message = "* Invalid password"
            return render_to_response("login/login.html", {
                "form": form,
                "error_message": error_message
            }, context_instance=RequestContext(request))

        return render_to_response("login/login.html", {
            "form": form
        }, context_instance=RequestContext(request))

    return render_to_response("login/login.html", {
        "form": form
    }, context_instance=RequestContext(request))


def forget_password(request):
    if request.user.is_authenticated():
         return redirect(settings.AFTER_LOGIN_REDIRECT_URL)

    form = EmailVerifyForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            token = get_random_string(length=11)
            password_reset_auth = PasswordResetAuth(choose_me=True, email=email, token=token)
            password_reset_auth.save()
            msg = SendEmail(request=request, file=[])
            msg.send_by_template(
                    recipient=[form.cleaned_data['email']],
                    template_path='login/changepassword_email.html',
                    context={
                        'reset_link': get_current_site(request).domain+"/login/reset-password/{}".format(token)
                    },
                    subject="Reset Password",
                )
            msg = SendEmail(request)
            return redirect("/login/")
    
    return render_to_response("login/forget-password.html", {
        "form":form
    }, context_instance=RequestContext(request))

def user_reset_password(request, token):
    """
        Function is used to reset the password of the user using the token identification
        which was created in forgot password.
    """

    if request.user.is_authenticated():
        return redirect(settings.AFTER_LOGIN_REDIRECT_URL)

    form = ResetPasswordForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user_auth = get_object_or_404(PasswordResetAuth, token=token)
            user = get_object_or_404(User, email=user_auth.email)

            if user_auth.choose_me is True:
                new_password = form.cleaned_data["new_password"]
                user.set_password(new_password)
                user.save()

                user_auth.choose_me = False
                user_auth.save()
                return redirect("/login/")

            error_message = "* Either you are not an identified user or "\
                "token has been expired. So please click on back."
            return render_to_response("login/reset_password.html", {
                "form": form,
                "error_message": error_message
            }, context_instance=RequestContext(request))

    return render_to_response("login/reset_password.html", {
        "form": form
    }, context_instance=RequestContext(request))



