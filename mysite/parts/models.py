# -*- coding: utf-8 -*-
from django.db import models
import datetime
import logging
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible
class Contact(models.Model):
    #=======销售===========
    yonghu = models.CharField(max_length=30,verbose_name="user")#用户单位
    yiqixinghao=models.CharField(max_length=30,verbose_name="type")#仪器型号
    yiqibh=models.CharField(max_length=30,verbose_name="sn")#仪器编号
    baoxiang =  models.CharField(max_length=30,verbose_name="pack")#包箱
    shenhe =  models.CharField(max_length=30,verbose_name="check")#审核
    yujifahuo_date = models.DateTimeField(verbose_name="send date")#预计发货时间
    hetongbh=models.CharField(max_length=30,verbose_name="contact sn")#合同编号
    def __str__(self):
        return str(self.id)+":"+self.hetongbh
@python_2_unicode_compatible    
class Item(models.Model):
    #ispack=models.BooleanField()
    bh = models.CharField(max_length=30,null=True,blank=True,verbose_name="sn")#库存编号
    name=models.CharField(max_length=30)#备件名称
    name_en=models.CharField(max_length=30,null=True,blank=True)#备件名称
    guige=models.CharField(max_length=30,null=True,blank=True,verbose_name="detail")#规格
    ct=  models.IntegerField(verbose_name="number",default=1)#数量
    danwei =  models.CharField(max_length=30,verbose_name="unit",default="个")#数量单位
    image=models.ImageField(null=True,blank=True,upload_to="item")
    def __str__(self):
        return str(self.id)+":"+self.name+"_"+self.guige+"_"+self.danwei
    class Admin:
        pass
@python_2_unicode_compatible 
class ContactItem(models.Model):
    contact=models.ForeignKey(Contact)#合同
    item=models.ForeignKey(Item)#备件
    ct=  models.IntegerField(verbose_name="number",default=1)#数量
    def __str__(self):
        return self.contact.hetongbh+"_"+self.item.name+"_"+self.item.guige+"_"+str(self.ct)+self.item.danwei
    class Admin:
        pass
class Test2(models.Model):
    ct=  models.IntegerField(verbose_name="number",default=1)#数量
    image=models.ImageField(null=True,upload_to="media")
    def __str__(self):
        return self.contact.hetongbh.encode("utf-8")+"_"+self.item.name.encode("utf-8")+"_"+self.item.guige.encode("utf-8")+"_"+str(self.ct)+self.item.danwei.encode("utf-8")
    class Admin:
        pass
        