from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from .views import login, show_user_report

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'centralization.views.home', name='home'),
    # url(r'^centralization/', include('centralization.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', login),
    (r'^centralization/userkeys/$', show_user_report),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^static', 'django.contrib.staticfiles.views.serve'),
)
