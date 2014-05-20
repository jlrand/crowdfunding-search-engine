from django.conf.urls.defaults import patterns, include, url

from crowdsearch import views

urlpatterns = patterns('',
    # ex: /crowdsearch/
    url(r'^$', views.index, name='index'),
    # ex: /crowdsearch/mostfunded/
    #url(r'^search/$', views.search, name='search'),
    # ex: /crowdsearch/mostbackers/
    url(r'^mostfunded/(?P<category>[^/]+)/$', views.mostfunded, name='mostfundedcategory'),
    # ex: /crowdsearch/mostbackers/
    url(r'^mostbackers/$', views.mostbackers, name='mostbackers'),
    # ex: /crowdsearch/reward/
    url(r'^mostbackers/(?P<category>[^/]+)/$', views.mostbackers, name='mostbackerscategory'),
    # ex: /crowdsearch/reward/
    url(r'^mostexpensive/$', views.mostexpensive, name='mostexpensive'),
    # ex: /crowdsearch/reward/
    url(r'^mostexpensive/(?P<category>[^/]+)/$',views.mostexpensive, name='mostexpensivecategory'),
    # ex: /crowdsearch/reward/
    url(r'^reward/$', views.mostpopularrewards, name='reward'),
    url(r'^mostbackedrewards/$', views.mostbackedrewards, name='mostbackedrewards'),
    url(r'^highrollers/$', views.highrollers, name='highrollers'),
    url(r'^reward/(?P<category>[^/]+)/$', views.mostpopularrewards, name='rewardcategory'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': '/home3/joninmal/public_html/uncrowdus/static'}),
)