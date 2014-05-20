from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from crowdsearch import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
    url(r'^search/', include('crowdsearch.urls')),
    url(r'^admin/', include(admin.site.urls)),
)