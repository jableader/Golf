from django.conf.urls import patterns, include, url
from django.contrib import admin
from GolfServer import views as golfviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'golf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', golfviews.home, name='home'),
    url(r'^login$', golfviews.login_form, name='login'),
    url(r'^logout$', golfviews.logout, name='logout'),
    url(r'users/profile/$', golfviews.profile, name='profile'),


    url(r'^admin/', include(admin.site.urls)),
)
