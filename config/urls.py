from django.conf.urls import patterns, include, url
from django.contrib import admin
from config import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'core.views.login_view', name='login'),
    url(r'^logout/', 'core.views.logout_view', name='logout'),
    url(r'^about/', 'core.views.about_view', name='about'),
    url(r'^show/create', 'core.views.create_show_view', name='create_show'),
    url(r'^change_log/', 'core.views.change_log_view', name='change_log'),
    url(r'^accept_change/(\d+)', 'core.views.accept_change_view', name='accept_change'),
    url(r'^filter_shows/', 'core.views.filter_shows_view', name='filter_show'),
    url(r'^account/create', 'core.views.create_account_view', name='create_account'),
    url(r'^account/successful','core.views.account_successful_view', name='account_successful'),
    url(r'^suggest_change/(\d+)','core.views.suggest_change_view', name='suggest_change'),
    url(r'^$','core.views.home_view', name='home'),
)