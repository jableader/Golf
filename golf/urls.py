from django.conf.urls import patterns, include, url
from django.contrib import admin
from golfsite import views as golfviews
from django.conf.urls.static import static
from . import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'golf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', golfviews.index, name='index'),
    url(r'^faq/$', golfviews.faq, name='faq'),
    url(r'^login/$', golfviews.login_form, name='login'),
    url(r'^logout/$', golfviews.logout, name='logout'),
    url(r'^users/profile/(?P<profile_pk>\d+)/$', golfviews.profile, name='profile'),
    url(r'^question/active/$', golfviews.question, name='active_question'),
    url(r'^question/(?P<question_pk>\d+)/$', golfviews.question, name='question'),
    url(r'^questions/(?P<page_number>\d+)/$', golfviews.questions, name='questions'),
    url(r'^questions/$', golfviews.questions, name='questions'),
    url(r'^submissions/make/(?P<question_pk>\d+)$', golfviews.upload_submission, name='make_submission'),
    url(r'^submissions/view/(?P<submission_pk>\d+)$', golfviews.view_submission, name='view_submission'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
