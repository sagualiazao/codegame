from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/captcha$', views.get_captcha),
    url(r'^api/reset-password-email$', views.reset_password_email),
    url(r'^api/check-email-captcha$', views.check_email_captcha),
    url(r'^api/reset-password$', views.reset_password),
    url(r'^api/register$', views.register),
    url(r'^api/login$', views.login),
    url(r'^api/logout$', views.logout),
    url(r'^api/check-email$', views.check_email),
    url(r'^api/save-map$', views.save_map),
    url(r'^api/read-map$', views.read_map),
    url(r'^api/pay$', views.pay),
    url(r'^api/read-map-list$', views.read_map_list),
    url(r'^api/change-favorite$', views.change_favorite_map),
    url(r'^api/read-published-map-list$', views.read_published_map_list),
    url(r'^api/read-favorite-map-list$', views.read_favorite_map_list)
]