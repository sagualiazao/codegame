from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/test$', views.test),
    url(r'^api/captcha-email$', views.captcha_email),
    url(r'^api/captcha$', views.get_captcha),
    url(r'^api/reset-password-mail$', views.reset_password_email),
    url(r'^api/reset-password$', views.reset_password),
    url(r'^api/register$', views.register)
]