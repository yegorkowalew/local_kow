from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'local_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^user/', include('userprofile.urls')),


    url(r'^admin/', include(admin.site.urls)),
#    url(r'', include('blog.urls')),
]
