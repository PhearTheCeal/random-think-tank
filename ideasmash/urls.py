from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ideasmash.views.home', name='home'),
    # url(r'^ideasmash/', include('ideasmash.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'derp.views.view_battle'),
    url(r'^battle/$', 'derp.views.view_battle'),
    url(r'^vote/$', 'derp.views.vote_battle'),
    url(r'^leaderboard/$', 'derp.views.view_leaderboard'),
    url(r'^addidea/$', 'derp.views.view_adder'),
    url(r'^add/$', 'derp.views.add_idea'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)
