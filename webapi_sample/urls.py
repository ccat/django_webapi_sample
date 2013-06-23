#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
#from django.conf.urls.i18n import i18n_patterns

from views import *

urlpatterns = patterns("",
    url(r"^nocredential/get/$", dataFromGETwithNoCredentialReturnJSON),
    url(r"^nocredential/post/$", dataFromPOSTwithNoCredentialReturnJSON),
    url(r"^nocredential/url/(?P<a>\d+)/(?P<b>\d+)/(?P<c>\d+)/$", dataFromURLwithNoCredentialReturnJSON),

    url(r"^withcredential/(?P<credential>\w+)/get/$", dataFromGETwithCredentialReturnJSON),
    url(r"^withcredential/(?P<credential>\w+)/post/$", dataFromPOSTwithCredentialReturnJSON),
    url(r"^withcredential/(?P<credential>\w+)/url/a(?P<a>\d+)/b(?P<b>\d+)/c(?P<c>\d+)/$", dataFromURLwithCredentialReturnJSON),
)



