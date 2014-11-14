from django.conf.urls import patterns, include, url
from django.contrib import admin
from GolfServer import views as golfviews
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'golf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include(golfviews.Home)),
    url(r'^admin/', include(admin.site.urls)),
)