from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        (r'^$','explore.views.index'),
)
