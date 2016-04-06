from django.conf.urls import include, url


urlpatterns = [
    # Examples:
    url(r'^$', 'login_utility.views.login_user', name='login_user'),
    url(r'^forget-password/', 'login_utility.views.forget_password', name="forget_password"),
    url(r'^reset-password/(?P<token>[a-zA-Z0-9]*)/$', 'login_utility.views.user_reset_password'),
    
]
