from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from mysite import settings
#from mysite.mygateway import echoGateway
admin.autodiscover()
#myconfig_download_url=r"/photo/"
#download_url="/download/"
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
urlpatterns = patterns('',
    # Example:
    (r'^$', 'mysite.mainview.index'),
    (r'^editor_index$', 'mysite.mainview.editor_index'),
    (r'^custom_editor$', 'mysite.mainview.custom_editor'),
    (r'^data_writer_test.php$', 'mysite.mainview.data_writer_test'),
    (r'^dtable_test.php$', 'mysite.mainview.dtable_test'),
    (r'^searching_test.php$', 'mysite.mainview.searching_test'),
    (r'^sorting_test.php$', 'mysite.mainview.sorting_test'),
    (r'^paging_test.php$', 'mysite.mainview.paging_test'),
    (r'^feeder.php$', 'mysite.mainview.feeder'),
    (r'^receiver.php$', 'mysite.mainview.receiver'),
    (r'^combo_test.php$', 'mysite.mainview.combo_test'),
    (r'^combo_test2.php$', 'mysite.mainview.combo_test2'),
    (r'^combo_test3.php$', 'mysite.mainview.combo_test3'),
    (r'^fetch_brands.php$', 'mysite.mainview.fetch_brands'),
    (r'^fetch_products.php$', 'mysite.mainview.fetch_products'),
	(r'^welcome$', 'mysite.mainview.welcome'),
    (r'^rest/',include('rest.urls')),   
    (r'^parts/',include('mysite.parts.urls')),   
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^gateway/', echoGateway),
    (r'^explore/',include('explore.urls')), 
    (r'^accounts/login/$', 'mysite.mainview.loginpage'),
    (r'^login/','mysite.mainview.mylogin'),  
    (r'^logout/','mysite.mainview.mylogout'),
    (r'^afterlogin/','mysite.mainview.afterlogin'),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL,view='django.contrib.staticfiles.views.serve')
