from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^user/', include('userprofile.urls')),
    url(r'^money/', include('money.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('userprofile.urls')),
]
