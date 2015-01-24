from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        (r'^$','rest.views.index'),
        (r'^index_2','rest.views.index_2'),
        (r'^application', 'rest.views.application'),
        (r'^item', 'rest.views.item'),
        (r'^contactitem', 'rest.views.contactitem'),
        (r'^contact', 'rest.views.contact'),
        (r'^login', 'rest.views.mylogin'),
        (r'^functions', 'rest.views.functions'),
        (r'^writer', 'rest.views.writer'),
	(r'^app.php_users_view$', 'rest.views.app_users_view'),
	(r'^app.php_users_create$', 'rest.views.app_users_create'),
	(r'^app.php_users_update$', 'rest.views.app_users_update'),
	(r'^app.php_users_destroy$', 'rest.views.app_users_destroy'),  
        (r'^view_item2$', 'rest.views.view_item2'),
        (r'^create_item2$', 'rest.views.create_item2'),
        (r'^update_item2$', 'rest.views.update_item2'),
        (r'^destroy_item2$', 'rest.views.destroy_item2'), 
        (r'^organize$', 'rest.views.organize'), 
        (r'^geticons$', 'rest.views.geticons'), 

)
