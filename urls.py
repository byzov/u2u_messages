from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'u2u_messages.views.all'),
    url(r'^all/(?P<username>[a-zA-Z0-9]+)$', \
            'u2u_messages.views.user'),
    url(r'^inbox/$', 'u2u_messages.views.all', {'type':'inbox'}),
    url(r'^send/$', 'u2u_messages.views.all', {'type':'send'}),
    url(r'^send_message$', 'u2u_messages.views.send'),
)
