# Django-auth
Django-auth is an easy method to provide your website a login and forget password functionality.

Quick start
-----------

1. Installation:

    `pip install git+https://github.com/technoarch-softwares/django-auth`

2. Add `"login_utility"` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (

        ...

        `'login_utility',`

    )
    

3. Run the migration command `python manage.py migrate`

4.   Add URL in your project urls
    
    `url(r'^login/', include('login_utility.urls')),`

5. Add Email Host Credentials in project settings file:-
    
    `DEFAULT_FROM_EMAIL_NAME = ''`
    `DEFAULT_FROM_EMAIL = ''`

    `EMAIL_HOST = ''`
    `EMAIL_PORT = `
    `EMAIL_HOST_USER = ''`
    `EMAIL_HOST_PASSWORD = ''`

6. Add a REDIRECT_URL for which you want to redirect after Login
     
    `AFTER_LOGIN_REDIRECT_URL = ""`

7. Enjoy the django-auth by visit http://127.0.0.1:8000/login/

