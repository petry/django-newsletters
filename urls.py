from django.conf.urls.defaults import *

urlpatterns = patterns('newsletters.views',
    url(r'^subscribe/$', 'subscribe', name='subscribe'),
    url(r'^subscribe/opt-in/$', 'subscribe_optin', name='subscription-opt-in'),
    url(r'^unsubscribe/$', 'unsubscribe', name='unsubscribe'),
    url(r'^unsubscribe/opt-out/$', 'unsubscribe_optin', name='unsubscription-opt-out'),
    url(r'^activate/(?P<activation_key>\w+)/$', 'activate', name='subscription-activate'),
    url(r'^deactivate/(?P<deactivation_key>\w+)/$', 'deactivate', name='subscription-deactivate'),
)