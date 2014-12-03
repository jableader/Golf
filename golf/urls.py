from django.conf.urls import patterns, include, url
from django.contrib import admin
from GolfServer import views as golfviews
from django.conf.urls.static import static
from . import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'golf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', golfviews.index, name='index'),
    url(r'^login/$', golfviews.login_form, name='login'),
    url(r'^logout/$', golfviews.logout, name='logout'),
    url(r'^users/profile/(?P<user_pk>\d+)/$', golfviews.profile, name='profile'),
    url(r'^question/(?P<question_pk>\d+)/$', golfviews.question, name='question'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)