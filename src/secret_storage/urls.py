from django.conf.urls import patterns, include, url

from django.contrib import admin
from secret_storage.shortcuts import views_rest
from secret_storage.views import BaseView
from security.views import csp_report
from django.conf import settings


admin.autodiscover()
views_rest.autodiscover()
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'secret_storage.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', BaseView.as_view()),
                       url(r'^api/', include(settings.API_ROUTER.urls)),
                       url(r'^csp-report', csp_report),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
