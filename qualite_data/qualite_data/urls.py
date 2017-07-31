from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
    url(r'^stat_cc_idf/', include('stat_cc_idf.urls')),
    url(r'^admin/', admin.site.urls),
]
