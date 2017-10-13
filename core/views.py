#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms

from models import User
from django.contrib.auth import authenticate

#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())


#注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            User.objects.create(username= username,password=password)
            return HttpResponse('regist success!!')
    else:
        uf = UserForm()
    return render(req,'regist.html',{'uf':uf})


#登录
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            A = uf.cleaned_data['username']
            B = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            #user = authenticate(username__exact = username,password__exact = password)
            #user = User.objects.filter(username__exact = username,password__exact = password)
            if A and B:
                #user = authenticate(username=username, password=password)
                user = User.objects.filter(username__exact=A, password__exact=B)
                #比较成功，跳转index

                if len(user)== 2:
                    #response = HttpResponseRedirect('/index/')
                    #response.set_cookie('username', username, 3600)
                    return render(req, 'index.html', {'uf': uf})
                else:
                    pass


            else:
                #比较失败，还在login
                pass
    else:
        uf = UserForm()
    return render(req, 'login.html', {'uf': uf})


#登陆成功
@login_required()
def index(req):
    username = req.COOKIES.get('username','')
    return render(req,'index.html' ,{'username':username})

#退出
def logout(req):
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response