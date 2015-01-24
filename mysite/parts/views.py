# Create your views here.
# -*- coding: utf-8 -*-
from mysite.parts.models import *
from django.shortcuts import render_to_response
import time
import os
import logging
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist#,DoesNotExist
from django.forms.models  import modelform_factory
import mysite.parts.models
from datetime import datetime
from django.forms import ModelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.context_processors import csrf
import json as simplejson
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mysite.parts.serializers import ItemSerializer,ContactSerializer,UserSerializer,ContactItemSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET', 'POST','DELETE'])
def user_list(request, format=None):
    """
    List all users, or create a new user.
    """
    logging.info("-============================")
    logging.info(request.method)
    logging.info(dir(request._request))
    logging.info(request._request)
    if request.method == 'GET':
        ct=User.objects.count()
        serializer = UserSerializer(User.objects.all(), many=True)
        out={"total":ct,"results":serializer.data}
        #logging.info(serializer.data)
        return Response(out)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            logging.info("save")
            serializer.save()
            serializer.data["clientId"]=request.DATA["id"]
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.info("not save")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        id1=request.DATA["id"]
        one=User.objects.get(id=int(id1))
        if one!=None:
            logging.info("save")
            one.delete()
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            logging.info("not save")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def item_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    logging.info(dir(request._request))
    logging.info(request._request)
    if request.method == 'GET':
        contact=int(request.GET.get("contact","0"))
        start=int(request.GET.get("start","0"))
        limit=int(request.GET.get("limit","5"))
        ct=ContactItem.objects.filter(contact=contact).count()
        snippets = ContactItem.objects.filter(contact=contact)[start:start+limit]
        serializer = ContactItemSerializer(snippets, many=True)
        out={"total":ct,"results":serializer.data}
        #logging.info(serializer.data)
        return Response(out)
    elif request.method == 'POST':
        serializer = ContactItemSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
@api_view(['GET', 'POST'])
def contact_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    logging.info(dir(request._request))
    logging.info(request._request)
    if request.method == 'GET':
        start=int(request.GET.get("start","0"))
        limit=int(request.GET.get("limit","5"))
        ct=Contact.objects.count()
        snippets = Contact.objects.all()[start:start+limit]
        serializer = ContactSerializer(snippets, many=True)
        out={"total":ct,"results":serializer.data}
        #logging.info(serializer.data)
        return Response(out)
    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def onepage(request):
    logging.info("onepage")
    objects=Contact.objects.all()
    paginator= Paginator(objects, 5)#contact number per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    r=render_to_response("parts/index.html",{"user":request.user,"contacts":contacts})
    return(r) 
def getCurrentContacts(request):        
    return request.user.contact_set.all()
 
def getCurrentUser(request):
    return request.user
def saveuser(request):
    bh=request.POST["username"]
    password=request.POST["password"]
    try:
        u=User.objects.get(username=bh)
    except ObjectDoesNotExist,e:
        u=User(username=bh)
        u.set_password(password)
        u.save()
        user = authenticate(username=bh, password=password)
        if user is not None:
            login(request, user)
            r=HttpResponseRedirect("/parts/afterlogin")
            return(r)
        else:
            return HttpResponse("login fail")
    else:
        err=bh+" already used by others"
        r=render_to_response("registration/register.html",{"err":err})
    return r
def register(request):
    r=render_to_response("registration/register.html")
    return r

    
def afterlogin(request):
    user=request.user
    dd=Group.objects.get(name="dd")
    if dd in user.groups.all():
        r=HttpResponseRedirect("/parts/")
    else:
        r=HttpResponseRedirect("/parts/")
    return(r)
#@staff_member_required
def loginpage(request):
    c={}
    c.update(csrf(request))
    r=render_to_response("registration/login.html",c)
    return(r)
def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    print username,password
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        r=HttpResponseRedirect("/parts/afterlogin")
        return(r)
        # Redirect to a success page.
    else:
        return HttpResponse("login faile")
        # Return an error message
def mylogout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")
def logout_user(http_request):
    logout(http_request)
 
def login_user(http_request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(http_request, user)
        return user
    return None
def items(request):
    logging.info("items")
    objects=Item.objects.all()
    paginator= Paginator(objects, 5)#contact number per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    r=render_to_response("parts/items.html",{"user":request.user,"contacts":contacts})
    return r
def index(request):
    logging.info("index")
    objects=Contact.objects.order_by('-yujifahuo_date').all()
    logging.info(objects)
    paginator= Paginator(objects, 5)#contact number per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    r=render_to_response("parts/dd_index.html",{"user":request.user,"contacts":contacts})
##    print dir(r)
    # r.headers["Pragma"]="No-cache"
    # r.headers["Cache-Control"]="no-cache"
    # r.headers["Expires"]="0"
##    print r.headers
    return(r)

def newcontact(request):
    dic = {}
    dic.update(csrf(request))
    dic["new"]="1"
    r=render_to_response("parts/newcontact.html",dic)
    return(r)

def savecontact(request):
    logging.info(request.POST)
    #===============
    new=request.POST["new"]

    yonghu=request.POST["yonghu"]
    yiqixinghao=request.POST["yiqixinghao"]
    yiqibh=request.POST["yiqibh"]
    baoxiang=request.POST["baoxiang"]
    shenhe=request.POST["shenhe"]
    yujifahuo_date=request.POST["yujifahuo_date"]
    hetongbh=request.POST["hetongbh"]

    if new=="1":
        c=Contact(yonghu=yonghu,yiqixinghao=yiqixinghao,yiqibh=yiqibh,baoxiang=baoxiang
        ,shenhe=shenhe,yujifahuo_date=yujifahuo_date,hetongbh=hetongbh
         )
        c.save()
    else:
        contact_id=request.POST["contact_id"]
        c=Contact.objects.get(id=contact_id)
        c.yonghu=yonghu
        c.yiqixinghao=yiqixinghao
        c.yiqibh=yiqibh
        c.baoxiang=baoxiang
        c.shenhe=shenhe
        c.yujifahuo_date=yujifahuo_date
        c.hetongbh=hetongbh
        c.save()
    r=HttpResponseRedirect("/parts/")
    return(r)

def editcontact(request):
    #print request.GET
    dic = {}
    dic.update(csrf(request))
    contact_id=request.GET["id"]
    c=Contact.objects.get(id=contact_id)
    dic["user"]=request.user
    dic["contact"]=c
    dic["new"]=0
    r=render_to_response("parts/newcontact.html",dic)
    return(r)

def deletecontact(request):
    print request.GET
    contact_id=request.GET["id"]
    c=Contact.objects.get(id=contact_id)
    c.delete()
    r=HttpResponseRedirect("/parts/")
    return(r)

def finishcontact(request):
    r=HttpResponseRedirect("/parts/")
    return(r)
def showcontact(request):
    #print request.GET
    dic = {}
    dic.update(csrf(request))
    contact_id=request.GET["id"]
    c=Contact.objects.get(id=contact_id)
    dic["user"]=request.user
    dic["contact"]=c
    dic["new"]=0
    r=render_to_response("parts/showcontact.html",dic)
    return(r)

# def showcontact(request):
#     contact_id=request.GET["id"]
#     eng=request.GET.get("english")
#     if eng==None:
#         eng="0"
#     contact=Contact.objects.get(id=contact_id)
#     if eng=="1":
#         s=u"用户名称:\t"+unicode(contact.yonghu)+"\n"
#         s+=u"仪器型号:\t"+contact.yiqixinghao+"\n"
#         s+=u"仪器编号:\t"+contact.yiqibh+"\n"
#         s+=u"包箱:\t"+contact.baoxiang+"\n"
#         s+=u"审核:\t"+contact.shenhe+"\n"
#         s+=u"预计发货时间:\t"+str(contact.yujifahuo_date)+"\n"
#         s+=u"合同编号:\t"+contact.hetongbh+"\n"
#         s+=u"库存编号\t配件名称\t规格\t数量\t备货\t审核\n"
#         for c in contact.contactitem_set.all(): 
#             s+=c.item.bh+"\t"+unicode(c.item.name_en)+"\t"+c.item.guige+"\t"+str(c.ct)+c.item.danwei+"\t\t\n"   
#     else:
#         s=u"用户名称:\t"+unicode(contact.yonghu)+"\n"
#         s+=u"仪器型号:\t"+contact.yiqixinghao+"\n"
#         s+=u"仪器编号:\t"+contact.yiqibh+"\n"
#         s+=u"包箱:\t"+contact.baoxiang+"\n"
#         s+=u"审核:\t"+contact.shenhe+"\n"
#         s+=u"预计发货时间:\t"+str(contact.yujifahuo_date)+"\n"
#         s+=u"合同编号:\t"+contact.hetongbh+"\n"
#         s+=u"sn\tname\t规格\tcount\tpack\t\n"
#         for c in contact.contactitem_set.all(): 
#             s+=c.item.bh+"\t"+c.item.name+"\t"+c.item.guige+"\t"+str(c.ct)+c.item.danwei+"\t\t\n"
#     r=HttpResponse()
#     r.content=s#.encode("gb2312")
#     return r

def printcontact(request):
    contact_id=request.GET["id"]
    eng=request.GET.get("english")
    if eng==None:
        eng="0"
    contact=Contact.objects.get(id=contact_id)
    if eng=="1":
        s=u"用户名称:\t"+unicode(contact.yonghu)+"\n"
        s+=u"仪器型号:\t"+contact.yiqixinghao+"\n"
        s+=u"仪器编号:\t"+contact.yiqibh+"\n"
        s+=u"包箱:\t"+contact.baoxiang+"\n"
        s+=u"审核:\t"+contact.shenhe+"\n"
        s+=u"预计发货时间:\t"+str(contact.yujifahuo_date)+"\n"
        s+=u"合同编号:\t"+contact.hetongbh+"\n"
        s+=u"库存编号\t配件名称\t规格\t数量\t备货\t审核\n"
        for c in contact.contactitem_set.all(): 
            s+=c.item.bh+"\t"+unicode(c.item.name_en)+"\t"+c.item.guige+"\t"+str(c.ct)+c.item.danwei+"\t\t\n"   
    else:
        s=u"用户名称:\t"+unicode(contact.yonghu)+"\n"
        s+=u"仪器型号:\t"+contact.yiqixinghao+"\n"
        s+=u"仪器编号:\t"+contact.yiqibh+"\n"
        s+=u"包箱:\t"+contact.baoxiang+"\n"
        s+=u"审核:\t"+contact.shenhe+"\n"
        s+=u"预计发货时间:\t"+str(contact.yujifahuo_date)+"\n"
        s+=u"合同编号:\t"+contact.hetongbh+"\n"
        s+=u"sn\tname\t规格\tcount\tpack\t\n"
        for c in contact.contactitem_set.all(): 
            s+=c.item.bh+"\t"+c.item.name+"\t"+c.item.guige+"\t"+str(c.ct)+c.item.danwei+"\t\t\n"
    r=HttpResponse(content_type="application/x-download")
    # print dir(r)
    # print r._headers
    # r._headers["content-type"]="application/x-download"
    r.content=s#.encode("gb2312")
    return r
def user_lists(request, username): 
    todo_lists = Contact.objects.all()
    return object_list(request, queryset=todo_lists) 

def server_processing(reauest):
    objs= Ajax.objects.all()
    output = {
        "sEcho" : 1,
        "iTotalRecords" : 1,
        "iTotalDisplayRecords" : 1,
        "aaData" : []
    }
    outdata=[]
    for  row in objs:
        outrow = []
        outrow.append(row.engine)# = models.CharField(max_length=30)
        outrow.append(row.browser)#=models.CharField(max_length=30,null=True)
        outrow.append(row.platform)#=models.CharField(max_length=30,null=True)
        outrow.append(row.version)#=models.FloatField()
        outrow.append(row.grade)#=models.CharField(max_length=30,null=True)
        outdata.append(outrow)
    output['aaData']= outdata
    return HttpResponse(simplejson.dumps(output, ensure_ascii=False))
def ajax(reauest):
    objs= Ajax.objects.all()
    a=objs[0].engine
    return HttpResponse(simplejson.dumps(a, ensure_ascii=False))
def post(request):
    logging.info("==========")
    logging.info(request.POST)
    objs= Ajax.objects.all()
    output = {
        "sEcho" : 1,
        "iTotalRecords" : 1,
        "iTotalDisplayRecords" : 1,
        "aaData" : []
    }
    outdata=[]
    for  row in objs:
        outrow = []
        outrow.append(row.engine)# = models.CharField(max_length=30)
        outrow.append(row.browser)#=models.CharField(max_length=30,null=True)
        outrow.append(row.platform)#=models.CharField(max_length=30,null=True)
        outrow.append(row.version)#=models.FloatField()
        outrow.append(row.grade)#=models.CharField(max_length=30,null=True)
        outdata.append(outrow)
    output['aaData']= outdata
    return HttpResponse(simplejson.dumps(output, ensure_ascii=False))
def editable_ajax(request):
    print "---"
    logging.debug(request.POST)
    print request.POST
    print request
    return HttpResponse(request.POST['value']+' (server updated)')
