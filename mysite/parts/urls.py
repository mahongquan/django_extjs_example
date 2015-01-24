from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	(r'^item_list/','mysite.parts.views.item_list'),
	(r'^contact_list/','mysite.parts.views.contact_list'),
        (r'^user_list/','mysite.parts.views.user_list'),

        (r'^$','mysite.parts.views.index'),
        (r'^items/','mysite.parts.views.items'),
                (r'^onepage/','mysite.parts.views.onepage'),
	(r'^register/','mysite.parts.views.register'),
	(r'^saveuser/','mysite.parts.views.saveuser'),	                       
	(r'^login/','mysite.parts.views.mylogin'),	
	(r'^logout/','mysite.parts.views.mylogout'),
	(r'^afterlogin/','mysite.parts.views.afterlogin'),
	(r'^loginpage/','mysite.parts.views.loginpage'),
         #
    (r'^showcontact/','mysite.parts.views.showcontact'),
	(r'^editcontact/','mysite.parts.views.editcontact'),
	(r'^newcontact/','mysite.parts.views.newcontact'),
	(r'^savecontact/','mysite.parts.views.savecontact'),
	(r'^printcontact/','mysite.parts.views.printcontact'),
	(r'^deletecontact/','mysite.parts.views.deletecontact'),                       
	(r'^finishcontact/','mysite.parts.views.finishcontact'),  

	(r'^server_processing/','mysite.parts.views.server_processing'),
    (r'^ajax/','mysite.parts.views.ajax'),       
    (r'^post/','mysite.parts.views.post'),           
         #
)
