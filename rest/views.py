# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
import time
import os
import logging
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import  check_password, make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist#,DoesNotExist
from django.forms.models  import modelform_factory
from datetime import datetime
from django.forms import ModelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.context_processors import csrf
from django.template.context import RequestContext
import mysite.settings
import datetime
import json
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from mysite.parts.models import Item,Contact,ContactItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import Group
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
    	if isinstance(obj,datetime.datetime):
            return "%d/%02d/%02d" % (obj.year,obj.month,obj.day)
        if isinstance(obj,Item):
            return obj.name
        if isinstance(obj,Contact):
            return obj.hetongbh        
        return json.JSONEncoder.default(self, obj)  
# class MyEncoderCh11(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, extjs.models.Ch11):
#             return {"id":obj.id,"name":obj.name,"gender":obj.gender,"dob":obj.dob,"epaper":obj.epaper}
#         if isinstance(obj,datetime.date):
#             return "%d/%02d/%02d" % (obj.year,obj.month,obj.day)
#         if isinstance(obj,Item):
#             return obj.name
#         if isinstance(obj,Contact):
#             return obj.hetongbh
#         return json.JSONEncoder.default(self, obj)  
def to_hash(u):
	return "{}"
def writer(request):
	# logging.info(request)
	# output={}
	# return HttpResponse(json.dumps(output, ensure_ascii=False))
	c=RequestContext(request,{})
	c.update(csrf(request))
	r=render_to_response("rest/writer.html",c)
	return(r)
@login_required
def app_users_view(request):
    start=int(request.GET.get("start","0"))
    limit=int(request.GET.get("limit","5"))
    total=User.objects.count()
    objs =User.objects.all()[start:start+limit]
    data=[]
    for rec in objs:
        data.append({"id":rec.id,"name":str(rec.username),"email":str(rec.email),"first":str(rec.first_name),"last":rec.last_name})
    logging.info(data)
    out={"total":total,"data":data}
    return HttpResponse(json.dumps(out, ensure_ascii=False,cls=MyEncoder))
@login_required    
def app_users_update(request):
    logging.info(request)
    request2=Request(request,(JSONParser(),))
    data = request2.DATA['data']
    id1=data["id"]
    rec=User.objects.get(id=id1)
    if data.get("name")!=None:
        rec.username=data["name"]
    if data.get("email")!=None:
        rec.email=data["email"]
    if data.get("first")!=None:
        rec.first_name=data["first"]
    if data.get("last")!=None:
        rec.last_name=data["last"]
    rec.save()
    output={"success":True,"message":"UPDATE new User" +str(rec.id)}
    output["data"]={"id":rec.id,"name":str(rec.username),"email":str(rec.email),"first":str(rec.first_name),"last":rec.last_name}
    return HttpResponse(json.dumps(output, ensure_ascii=False))
@login_required    
def app_users_destroy(request):
    logging.info(request)
    request2=Request(request,(JSONParser(),))
    data = request2.DATA['data']
    id1=data["id"]
    rec=User.objects.get(id=id1)
    rec.delete()
    output={"success":True,"message":"delete User" +str(rec.id)}
    output["data"]={"id":id1}#,"name":str(rec.username),"email":str(rec.email),"first":str(rec.first_name),"last":rec.last_name}
    return HttpResponse(json.dumps(output, ensure_ascii=False))
@login_required
def app_users_create(request):
    logging.info(request)
    request2=Request(request,(JSONParser(),))
    data = request2.DATA['data']
    rec=User()#.objects.get(id=id1)
    if data.get("name")!=None:
        rec.username=data["name"]
    if data.get("email")!=None:
        rec.email=data["email"]
    if data.get("first")!=None:
        rec.first_name=data["first"]
    if data.get("last")!=None:
        rec.last_name=data["last"]
    rec.save()
    output={"success":True,"message":"create new User" +str(rec.id)}
    output["data"]={"id":rec.id,"name":str(rec.username),"email":str(rec.email),"first":str(rec.first_name),"last":rec.last_name}
    return HttpResponse(json.dumps(output, ensure_ascii=False))

def index(request):
	c=RequestContext(request,{"user":request.user})
	c.update(csrf(request))
	r=render_to_response("rest/restful.html",c)
	return(r)
def index_2(request):
	# logging.info(request)
	# output={}
	# return HttpResponse(json.dumps(output, ensure_ascii=False))
	c=RequestContext(request,{})
	c.update(csrf(request))
	r=render_to_response("rest/index_2.html",c)
	return(r) 
@login_required
def item(request):
	logging.info("===================")
	logging.info(request)
	logging.info("------------------")
	request2=Request(request,(JSONParser(),))
	logging.info(request2)
	if request.method == 'GET':
		return view_item(request2)
	if request.method == 'POST':
		return create_item(request2)
	if request.method == 'PUT':
		return update_item(request2)
	if request.method == 'DELETE':
		return destroy_item(request2)	
@login_required
def application(request):
	logging.info("===================")
	logging.info(request)
	logging.info("------------------")
	request2=Request(request,(JSONParser(),))
	logging.info(request2)
	if request.method == 'GET':
		return view(request2)
	if request.method == 'POST':
		return create(request2)
	if request.method == 'PUT':
		return update(request2)
	if request.method == 'DELETE':
		return destroy(request2)
def view(request):
	objs=User.objects.all()
	data=[]
	for obj in objs:
		data.append({"id":obj.id,"email":obj.email,"username":obj.username})
	output={"data":data}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def create(request):
	f=request.META["wsgi.input"]
	logging.info(dir(f))
	data="---"
	logging.info(data)
 	rec=User()
 	rec.username=request.DATA["username"]
 	rec.email=request.DATA["email"]
	rec.save()
	output={"success":True,"message":"Created new User" +str(rec.id)}
	output["data"]={"id":rec.id,"email":rec.email,"username":rec.username}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def update(request):
	id1=int(request.DATA["id"])
	rec=User.objects.get(id=id1)
	if request.DATA.get("username")!=None:
 		rec.username=request.DATA["username"]
 	if request.DATA.get("email")!=None:
 		rec.email=request.DATA["email"]
	rec.save()
	output={"success":True,"message":"Created new User" +str(rec.id)}
	output["data"]={"id":rec.id,"email":rec.email,"username":rec.username}
	return HttpResponse(json.dumps(output, ensure_ascii=False))

def destroy(request):
	id=request.path.split("/")[-1]
	id1=int(id)
	rec=User.objects.get(id=id1)
	rec.delete()
	output={"success":True,"message":"OK"}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def view_item(request):
	logging.info("here")
	start=int(request.GET.get("start","0"))
	limit=int(request.GET.get("limit","5"))
	search=request.GET.get("search",'')
	search_bh=request.GET.get("search_bh",'')
	logging.info("search="+search)
	if search!='':
		if search_bh!='':
			total=Item.objects.filter(name__contains=search).filter(bh__contains=search_bh).count()
		 	objs = Item.objects.filter(name__contains=search).filter(bh__contains=search_bh)[start:start+limit]
		else:
			total=Item.objects.filter(name__contains=search).count()
		 	objs = Item.objects.filter(name__contains=search)[start:start+limit]
	else:
		if search_bh!='':
			total=Item.objects.filter(bh__contains=search_bh).count()
		 	objs = Item.objects.filter(bh__contains=search_bh)[start:start+limit]
		else:
			total=Item.objects.count()
		 	objs = Item.objects.all()[start:start+limit]
	data=[]
	for rec in objs:
		data.append({"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei})
	logging.info(data)
	out={"total":total,"data":data}
	return HttpResponse(json.dumps(out, ensure_ascii=False,cls=MyEncoder))
def create_item(request):
	f=request.META["wsgi.input"]
	logging.info(dir(f))
	data="---"
	logging.info(data)
 	rec=Item()
 	rec.name=request.DATA["name"]
 	rec.bh=request.DATA["bh"]
 	rec.guige=request.DATA["guige"]
 	rec.danwei=request.DATA["danwei"]
	rec.save()
	output={"success":True,"message":"Created new User" +str(rec.id)}
	output["data"]={"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def update_item(request):
	id1=int(request.DATA["id"])
	rec=Item.objects.get(id=id1)
	if request.DATA.get("bh")!=None:
 		rec.bh=request.DATA["bh"]
 	if request.DATA.get("name")!=None:
 		rec.name=request.DATA["name"]
 	if request.DATA.get("guige")!=None:
 		rec.guige=request.DATA["guige"]
 	if request.DATA.get("danwei")!=None:
 		rec.danwei=request.DATA["danwei"]
	rec.save()
	output={"success":True,"message":"update item " +str(rec.id)}
	output["data"]={"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
	objs=User.objects.all()
	data=[]
	for rec in objs:
		data.append({"id":rec.id,"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang})
	output={"data":data}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def destroy_item(request):
	id=request.path.split("/")[-1]
	id1=int(id)
	rec=Item.objects.get(id=id1)
	rec.delete()
	output={"success":True,"message":"OK"}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
@login_required
def contact(request):
	logging.info("===================")
	logging.info(request)
	logging.info("------------------")
	request2=Request(request,(JSONParser(),))
	logging.info(request2)
	if request.method == 'GET':
		return view_contact(request2)
	if request.method == 'POST':
		return create_contact(request2)
	if request.method == 'PUT':
		return update_contact(request2)
	if request.method == 'DELETE':
		return destroy_contact(request2)
def view_contact(request):
	objs=Contact.objects.order_by('-yujifahuo_date').all()
	data=[]
	for rec in objs:
		data.append({"id":rec.id,"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang})
	output={"data":data}
	return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
def create_contact(request):
 	rec=Contact()
 	#"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang"
 	rec.hetongbh=request.DATA["hetongbh"]
 	logging.info(request.DATA["yujifahuo_date"])
 	d=datetime.datetime.fromtimestamp(int(request.DATA["yujifahuo_date"]))
 	logging.info(d)
 	rec.yujifahuo_date=d
 	logging.info(rec.yujifahuo_date)
 	rec.yonghu=request.DATA["yonghu"]
 	rec.baoxiang=request.DATA["baoxiang"]
 	rec.save()
	output={"success":True,"message":"Created new User" +str(rec.id)}
	output["data"]={"id":rec.id,"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang}
	return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
def update_contact(request):
	id1=int(request.DATA["id"])
	rec=Contact.objects.get(id=id1)
	if request.DATA.get("hetongbh")!=None:
 		rec.hetongbh=request.DATA["hetongbh"]
 	if request.DATA.get("yujifahuo_date")!=None:
 		rec.yujifahuo_date=d=datetime.datetime.fromtimestamp(int(request.DATA["yujifahuo_date"]))
 	if request.DATA.get("yonghu")!=None:
 		rec.yonghu=request.DATA.get("yonghu")
 	if request.DATA.get("baoxiang")!=None:
 		rec.baoxiang=request.DATA.get("baoxiang")
	rec.save()
	output={"success":True,"message":"update Contact " +str(rec.id)}
	output["data"]={"id":rec.id,"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang}
	return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
	
def destroy_contact(request):
	id=request.path.split("/")[-1]
	id1=int(id)
	rec=Contact.objects.get(id=id1)
	rec.delete()
	output={"success":True,"message":"OK"}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def mylogin(request):
	logging.info(request)
	request2=Request(request,(JSONParser(),))
	data = request2.POST
	username = data['username']
	password = data['password']
	user = authenticate(username=username, password=password)
	if user is None:
		output={"success":False,"message":"No This User"}
	else:
		login(request, user)
		rec=user
		output={"success":True,"message":"User" +str(rec.id)}
		output["data"]={"id":rec.id,"name":str(rec.username),"email":str(rec.email),"first":str(rec.first_name),"last":rec.last_name}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def functions(request):
	logging.info("===================")
	logging.info(request)
	logging.info("------------------")
	request2=Request(request,(JSONParser(),))
	logging.info(request2)
	if request.method == 'GET':
		return view(request2)
	if request.method == 'POST':
		return create(request2)
	if request.method == 'PUT':
		return update(request2)
	if request.method == 'DELETE':
		return destroy(request2)
@login_required
def contactitem(request):
	logging.info("===================")
	logging.info(request)
	logging.info("------------------")
	request2=Request(request,(JSONParser(),))
	logging.info(request2)
	if request.method == 'GET':
		return view_contactitem(request2)
	if request.method == 'POST':
		return create_contactitem(request2)
	if request.method == 'PUT':
		return update_contactitem(request2)
	if request.method == 'DELETE':
		return destroy_contactitem(request2)	
def view_contactitem(request):
	contact=int(request.GET.get("contact","0"))
	start=int(request.GET.get("start","0"))
	limit=int(request.GET.get("limit","5"))
	total=ContactItem.objects.filter(contact=contact).count()
 	objs = ContactItem.objects.filter(contact=contact)[start:start+limit]
	# objs=ContactItem.objects.filter(contact=3)
	data=[]
	for rec in objs:
		logging.info(rec.item)
		#data.append({"id":rec.id,"contact":str(rec.contact.id)+":"+rec.contact.hetongbh,"item":str(rec.item.id)+":"+rec.item.name,"ct":rec.ct})
		data.append({"id":rec.id,"contact":str(rec.contact.id),"item":str(rec.item.id),"ct":rec.ct,"hetongbh":rec.contact.hetongbh,"name":rec.item.name})
	logging.info(data)
	out={"total":total,"results":data}
	return HttpResponse(json.dumps(out, ensure_ascii=False,cls=MyEncoder))
def create_contactitem(request):
 	rec=ContactItem()
 	#"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang"
 	if(request.DATA.get("contact")!=None and request.DATA.get("item")!=None and request.DATA.get("ct")!=None):
	 	rec.contact=Contact.objects.get(id=int(request.DATA["contact"]))
	 	rec.item=Item.objects.get(id=int(request.DATA["item"]))
	 	rec.ct=int(request.DATA["ct"])
	 	rec.save()
		output={"success":True,"message":"Created new User" +str(rec.id)}
		output["data"]={"id":rec.id,"contact":str(rec.contact.id),"item":str(rec.item.id),"ct":rec.ct,"hetongbh":rec.contact.hetongbh,"name":rec.item.name}
		return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
	else:
		output={"success":False,"message":"No enough parameters"}
		output["data"]={}
		return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
def update_contactitem(request):
	id1=int(request.DATA["id"])
	rec=ContactItem.objects.get(id=id1)
	if request.DATA.get("contact")!=None:
 		rec.contact=request.DATA["contact"]
 	if request.DATA.get("item")!=None:
 		rec.item=request.DATA["item"]
 	if request.DATA.get("ct")!=None:
 		rec.ct=request.DATA["ct"]
	rec.save()
	output={"success":True,"message":"update ContactItem " +str(rec.id)}
	output["data"]={"id":rec.id,"contact":str(rec.contact.id),"item":str(rec.item.id),"ct":rec.ct,"hetongbh":rec.contact.hetongbh,"name":rec.item.name}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
def destroy_contactitem(request):
	#id=request.path.split("/")[-1]
	id1=int(request.DATA["id"])
	rec=ContactItem.objects.get(id=id1)
	rec.delete()
	output={"success":True,"message":"OK"}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
#ajax method####################################################################
@login_required
def view_item2(request):
	logging.info("here")
	start=int(request.GET.get("start","0"))
	limit=int(request.GET.get("limit","5"))
	search=request.GET.get("search",'')
	search_bh=request.GET.get("search_bh",'')
	logging.info("search="+search)
	if search!='':
		if search_bh!='':
			total=Item.objects.filter(name__contains=search).filter(bh__contains=search_bh).count()
		 	objs = Item.objects.filter(name__contains=search).filter(bh__contains=search_bh)[start:start+limit]
		else:
			total=Item.objects.filter(name__contains=search).count()
		 	objs = Item.objects.filter(name__contains=search)[start:start+limit]
	else:
		if search_bh!='':
			total=Item.objects.filter(bh__contains=search_bh).count()
		 	objs = Item.objects.filter(bh__contains=search_bh)[start:start+limit]
		else:
			total=Item.objects.count()
		 	objs = Item.objects.all()[start:start+limit]
	data=[]
	for rec in objs:
		data.append({"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei})
	logging.info(data)
	out={"total":total,"data":data}
	return HttpResponse(json.dumps(out, ensure_ascii=False,cls=MyEncoder))
@login_required
def create_item2(request):
	request=Request(request,(JSONParser(),))
	logging.info(request.DATA)
	datas=request.DATA["data"]
	logging.info(datas)
	output={"success":True,"message":"Created new User"}
	if type(datas) is list:
		output["data"]=[]
		for data in datas:
		 	rec=Item()
		 	rec.name=data["name"]
		 	rec.bh=data["bh"]
		 	rec.guige=data["guige"]
		 	rec.danwei=data["danwei"]
			rec.save()
			output["data"].append({"clientId":data["id"],"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei})
	else:
		data=datas
	 	rec=Item()
	 	rec.name=data["name"]
	 	rec.bh=data["bh"]
	 	rec.guige=data["guige"]
	 	rec.danwei=data["danwei"]
		rec.save()
		output["data"]={"clientId":data["id"],"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
	#not batch
	# request=Request(request,(JSONParser(),))
	# logging.info(request.DATA)
	# data=request.DATA["data"]
 # 	rec=Item()
 # 	rec.name=data["name"]
 # 	rec.bh=data["bh"]
 # 	rec.guige=data["guige"]
 # 	rec.danwei=data["danwei"]
	# rec.save()
	# output={"success":True,"message":"Created new User" +str(rec.id)}
	# output["data"]={"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
	# return HttpResponse(json.dumps(output, ensure_ascii=False))
@login_required
def update_item2(request):
	request=Request(request,(JSONParser(),))
	datas=request.DATA["data"]
	output={"success":True,"message":"update item "}
	if type(datas) is list:
		output["data"]=[]
		for data in datas:
			id1=int(data["id"])
			rec=Item.objects.get(id=id1)
			if data.get("bh")!=None:
		 		rec.bh=data["bh"]
		 	if data.get("name")!=None:
		 		rec.name=data["name"]
		 	if data.get("guige")!=None:
		 		rec.guige=data["guige"]
		 	if data.get("danwei")!=None:
		 		rec.danwei=data["danwei"]
			rec.save()
			output["data"].append({"clientId":data["id"],"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei})
	else:
		data=datas
		id1=int(data["id"])
		rec=Item.objects.get(id=id1)
		if data.get("bh")!=None:
	 		rec.bh=data["bh"]
	 	if data.get("name")!=None:
	 		rec.name=data["name"]
	 	if data.get("guige")!=None:
	 		rec.guige=data["guige"]
	 	if data.get("danwei")!=None:
	 		rec.danwei=data["danwei"]
		rec.save()
		output["data"]={"clientId":data["id"],"id":rec.id,"bh":rec.bh,"name":rec.name,"guige":rec.guige,"danwei":rec.danwei}
	return HttpResponse(json.dumps(output, ensure_ascii=False))
	# objs=User.objects.all()
	# data=[]
	# for rec in objs:
	# 	data.append({"id":rec.id,"hetongbh":rec.hetongbh,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang})
	# output={"data":data}
	# return HttpResponse(json.dumps(output, ensure_ascii=False))
@login_required
def destroy_item2(request):
	request=Request(request,(JSONParser(),))
	datas=request.DATA["data"]
	if type(datas) is list:
		for data in datas:
			id1=int(data["id"])
			rec=Item.objects.get(id=id1)
			rec.delete()
	else:
		data=datas
		id1=int(data["id"])
		rec=Item.objects.get(id=id1)
		rec.delete()
	output={"success":True,"message":"OK"}
	return HttpResponse(json.dumps(output, ensure_ascii=False))

def organize(request):
	c=RequestContext(request,{})
	c.update(csrf(request))
	r=render_to_response("rest/organizer.html",c)
	return(r)
def geticons(request):
	logging.info("here")
	start=int(request.GET.get("start","0"))
	limit=int(request.GET.get("limit","5"))
	search=request.GET.get("search",'')
	search_bh=request.GET.get("search_bh",'')
	logging.info("search="+search)
	if search!='':
		if search_bh!='':
			total=Item.objects.filter(name__contains=search).filter(bh__contains=search_bh).count()
		 	objs = Item.objects.filter(name__contains=search).filter(bh__contains=search_bh)[start:start+limit]
		else:
			total=Item.objects.filter(name__contains=search).count()
		 	objs = Item.objects.filter(name__contains=search)[start:start+limit]
	else:
		if search_bh!='':
			total=Item.objects.filter(bh__contains=search_bh).count()
		 	objs = Item.objects.filter(bh__contains=search_bh)[start:start+limit]
		else:
			total=Item.objects.count()
		 	objs = Item.objects.all()[start:start+limit]
	data=[]
	for rec in objs:
		data.append({"id":rec.id,"thumb":rec.image.name,"name":rec.name})
	logging.info(data)
	return HttpResponse(json.dumps(data, ensure_ascii=False,cls=MyEncoder))
	# output=[
	#     {
	#         "name": "说明书",
	#         "thumb": "20140326_015.jpg",
	#         "url": "kitchensink",
	#         "type": "Application"
	#     },
	#     {
	#         "name": "坩埚",
	#         "thumb": "0102g001004.JPG",
	#         "url": "twitter",
	#         "type": "Application"
	#     },
	#     {
	#         "name": "真空硅脂",
	#         "thumb": "0102g001009.JPG",
	#         "url": "kiva",
	#         "type": "Application"
	#     },
	#     {
	#         "name": "铜管",
	#         "thumb": "0103a005011.JPG",
	#         "url": "geocongress",
	#         "type": "Application"
	#     }
	# ]
	# return HttpResponse(json.dumps(output, ensure_ascii=False))	