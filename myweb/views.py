from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib import auth
from myweb.models import Module
from myweb.models import Buser
from myweb.models import Bmap
import json
from django.core import serializers

from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
User = get_user_model()

# Create your views here.

def index(request):
    return render(request,
                  template_name='index.html')


def account_show(request):
    users_temp = User.objects.all()
    d_users = {}
    for i in range(len(users_temp)):
        d_users[i] = model_to_dict(users_temp[i])
        user_permissions = []
        for j in range(len(d_users[i]['user_permissions'])):
            tmp = d_users[i]['user_permissions'][j].name
            user_permissions.append(tmp)
        d_users[i]['user_permissions'] = user_permissions
    if d_users:
        return render(request, 'account_Inquiry.html',
                      {'d_users': json.dumps(d_users, cls=DjangoJSONEncoder)})
    else:
        return render(request, 'account_Inquiry.html', {'message': '查找结果为空！'})


def account_inquiry(request):
    message = request.POST.get('message', False)
    fuzzy_search(message)
    users_temp=fuzzy_search(message)
    users = {}
    for i in range(len(users_temp)):
        users[i] = model_to_dict(users_temp[i])
        user_permissions = []
        for j in range(len(users[i]['user_permissions'])):
            tmp = users[i]['user_permissions'][j].name
            user_permissions.append(tmp)
        users[i]['user_permissions'] = user_permissions
    if users:
        return render(request, 'account_Inquiry.html', {'d_users': json.dumps(users, cls=DjangoJSONEncoder)})
    else:
        return render(request, 'account_Inquiry.html', {'message': '查找结果为空！'})


def add_Account(request):
    return render(request,
                  template_name='add_Account.html')


def add_usr(request):
    username = request.POST.get("username", False)
    enterprise_name= request.POST.get("enterprise_name", False)
    contact_usr= request.POST.get("contact_usr", False)
    phone= request.POST.get("phone", False)
    user_type = request.POST.get("user_type", False)
    check_box = request.POST.getlist('check_box', False)
    #check_box = json.loads(check_box)
    permission_dict = {'1': "city_management", '2': "agriculture_management", '3': "forestry_management",
                       '4': "environment_management",'5': "road_management",'6': "settlement_observation"}
    user = User.objects.create_user(username=username, enterprise_name=enterprise_name, usr_type=user_type,
                                    contact_usr=contact_usr, phone=phone)
    user.save()
    for i in check_box:
        permission = Permission.objects.get(codename=permission_dict[i])
        user.user_permissions.add(permission)
    return render(request,'add_Account.html',{'message':'添加成功'})



def _permissions_query(request):
    message = request.POST.get('message',False)
    query_method = request.POST.get('query_method', False)
    users_temp = []
    if query_method == '1':
        users_temp = User.objects.filter(username=message)
    if query_method == '2':
        users_temp = User.objects.filter(department_name=message)
    if query_method == '3':
        users_temp = User.objects.filter(phone=message)
    if query_method == '4':
        users_temp = User.objects.filter(contact_usr=message)
    users={}
    for i in range(len(users_temp)):
       users[i]=model_to_dict(users_temp[i])
       user_permissions = []
       for j in range(len(users[i]['user_permissions'])):
           tmp = users[i]['user_permissions'][j].name
           user_permissions.append(tmp)
       users[i]['user_permissions'] = user_permissions
    if users:
        return render(request,'permissions_query.html',locals())
    else:
        return render(request,'permissions_query.html',{'message1':'查找结果为空！'})



def upload_map(request):
    return render(request,
                  template_name='upload_map.html')

def password_revise(request):
    return render(request,
                  template_name='password_revise.html')



def _upload_map(request):
    map_name = request.POST.get("map_name", False)
    satelite= request.POST.get("satelite", False)
    desc=request.POST.get("desc", False)
    wholemap= request.POST.get("wholemap", False)
    thumbnail= request.POST.get("thumbnail", False)
    map = Bmap.objects.create(map_name=map_name, satelite=satelite,desc=desc,wholemap_path=wholemap,thumbnail_path=thumbnail)
    map.save()
    return render(request,'upload_map.html',{'message':'上传成功'})


def deliver_map(request):
    maps_temp = Bmap.objects.all()
    d_maps = {}
    for i in range(len(maps_temp)):
        d_maps[i] = model_to_dict(maps_temp[i])
    if d_maps:
      return HttpResponse(json.dumps({'d_maps': json.dumps(d_maps, cls=DjangoJSONEncoder)}))
    else:
      return HttpResponse(json.dumps({'message': '查找结果为空！'}))

def fuzzy_search(message):
    list1=[]
    user1=list(User.objects.filter(username=message))
    user2 =list(User.objects.filter(enterprise_name=message))
    user3 = list(User.objects.filter(usr_type=message))
    user4 = list(User.objects.filter(contact_usr=message))
    user5 = list(User.objects.filter(phone=message))
    users=((((list1.extend(user1)).extend(user2)).extend(user3)).extend(user4)).extend(user5)
    users_sorted = list(set(users))
    users_sorted.sort(key=users.index)
    return users_sorted

def info_revise(request):
    username=request.POST.get("username", False)
    return render(request, 'info_revise.html', {'username': username})

def sinfo_revise(request):
    return render(request, template_name='info_revise.html')


def _info_revise(request):
        username = request.POST.get("username", False)
        enterprise_name = request.POST.get("enterprise_name", False)
        contact_usr = request.POST.get("contact_usr", False)
        phone = request.POST.get("phone", False)
        usr_type=request.POST.get("usr_type", False)
        user = User.objects.get(username=username)
        if user:
            user.enterprise_name= enterprise_name
            user.usr_type = usr_type
            user.phone = phone
            user.contact_usr =contact_usr
            user.save()
            return render(request, 'info_revise.html', {'message': '修改成功！'})

        else:
            return render(request, 'info_revise.html',{'message': '用户不存在！'})

def _account_show(request):
    users_temp = User.objects.all()
    d_users = {}
    for i in range(len(users_temp)):
        d_users[i] = model_to_dict(users_temp[i])
        user_permissions = []
        for j in range(len(d_users[i]['user_permissions'])):
            tmp = d_users[i]['user_permissions'][j].name
            user_permissions.append(tmp)
        d_users[i]['user_permissions'] = user_permissions
    if d_users:
        return render(request, 'authorityManagement.html',{'d_users': json.dumps(d_users, cls=DjangoJSONEncoder)})
    else:
        return render(request, 'authorityManagement.html', {'message': '查找结果为空！'})

def status_revise(request):
    #raw_dic=request.raw_post_data()
    #dic=json.loads(raw_dic,cls=DjangoJSONEncoder)
    is_active=request.POST.get('is_active', False)
    id=request.POST.get('id', False)
    user=User.objects.get(id=id)
    user.is_active=is_active
    user.save()
    return render(request,'authorityManagement.html',{'userid':id,'isactive':is_active})

def permission_revise(request):
    userid = request.POST.get("id", False)
    check_box = request.POST.get('permission_value',False)
    check_box=json.loads(check_box)
    user = User.objects.get(id=userid)
    user.user_permissions.clear()
    permission_dict={'1': "city_management", '2': "agriculture_management", '3': "forestry_management",
                       '4': "environment_management",'5': "road_management",'6': "settlement_observation"}
    for i in check_box:
       permission = Permission.objects.get(codename=permission_dict[i])
       user.user_permissions.add( permission )
    user=model_to_dict(user)
    user_permissions = []
    for j in range(len(user['user_permissions'])):
        tmp = user['user_permissions'][j].name
        user_permissions.append(tmp)

    return HttpResponse(json.dumps({"new_permissions":user_permissions}))

def password_reset(request):
    old_password = request.POST.get("old_password",False)
    new_password = request.POST.get("new_password1",False)
    if request.user.check_password(old_password):
        request.user.set_password(new_password)
        request.user.save()

        return render(request, 'password_revise.html', {'message': '修改成功！'})
    else:
        return render(request, 'password_revise.html',{'message': '用户名或密码错误!'})

def _sinfo_revise(request):
        username = request.POST.get("username", False)
        enterprise_name = request.POST.get("enterprise_name", False)
        contact_usr = request.POST.get("contact_usr", False)
        phone = request.POST.get("phone", False)
        usr_type = request.POST.get("usr_type", False)
        user = User.objects.get(username=username)
        if user:
            user.enterprise_name = enterprise_name
            user.usr_type = usr_type
            user.phone = phone
            user.contact_usr = contact_usr
            user.save()
            return render(request, 'info_revise.html', {'message': '修改成功！'})
        else:
            return render(request, 'info_revise.html', {'message': '用户不存在！'})
