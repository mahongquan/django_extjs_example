# -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers
from mysite.parts.models import *
from django.contrib.auth.models import User
# baoxiang =  models.CharField(max_length=30,verbose_name="pack")#包箱
#     shenhe =  models.CharField(max_length=30,verbose_name="check")#审核
#     yujifahuo_date = models.DateTimeField(verbose_name="send date")#预计发货时间
#     hetongbh=models.CharField(max_length=30,verbose_name="contact sn")#合同编号
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model = User
        fields = ('id', 'username','email')
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id' ,'yonghu','yiqixinghao','baoxiang','shenhe','yujifahuo_date','hetongbh')
# class ContactItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContactItem
#         fields = ('id' ,'item','ct')
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id',  'bh','name')
    #      measure=models.ForeignKey(Measure,db_column=u'measureid')#设备
    # comm_date = models.DateTimeField(db_column=u'测量时间')
    # top = models.FloatField(db_column=u'温度上')#地址
    # middle = models.FloatField(db_column=u'温度中')#地址
    # bottom = models.FloatField(db_column=u'温度下')#地址
    # paraID = models.IntegerField(db_column=u'paraID')#地址
class ContactItemSerializer(serializers.Serializer):
    #pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    id = serializers.IntegerField()
    item = serializers.IntegerField()
    ct = serializers.IntegerField()
    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.item = attrs.get('title', instance.item)
            instance.ct = attrs.get('code', instance.ct)
            return instance

        # Create new instance
        return ContactItem(**attrs)
