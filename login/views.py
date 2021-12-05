
# Create your views here.
from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.views import APIView,AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db import connection
import json

# Create your views here.
# 用户注册
#在内置的User中username,定义为email
class Register(APIView):
    def post(self,request, *args, **kwargs):
        if request.method == 'POST':

            print("receive POST request at /register")
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            username = data.get('name')
            mobile = data.get('mobile')
            province = data.get('province')
            city = data.get('city')
            address = data.get('address')

            if User.objects.filter(username=email).exists():
                resp = {
                    'id': -1,
                    'msg': 'Username already exists',
                    'payload': [],
                }
            else:
                user = User.objects.create_user(username=email, password=password)
                with connection.cursor() as cur:
                    cur.execute()

                resp = {
                    'id': 0,
                    'msg': 'Success',
                }

        return Response(resp)

# 用户登录
class Login(APIView):
    def post(self,request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /login")
            data = json.loads(request.body)
            print(data)

            username = data.get('username')
            password = data.get('password')
            print(username)
            print(password)
            #   内置验证
            #   username = auth.authenticate(username = username, password = password)

            n = authenticate(username=username, password=password)
            if n:
                # 登陆成功即可获取当前登录用户，返回主页
                auth.login(request, user=n)
                #return
                resp = {
                    'id': 0,
                    'msg': 'Success',
                    'payload':[]
                }
                return Response(resp)
        # 失败重定向到登录页
            #test----------------------------------------------
            else:
                resp = {
                    'id': -1,
                    'msg': 'username doesnot exist',
                    'payload':
                        {
                            "username": "A",
                            "mobile": "10.46.233.207",
                            "province": "D",
                            "city": "1",
                            "address": "1"
                        }
                }
                return Response(resp)
            #test----------------------------------------------
        #return
        return redirect('/api/test/')


class Test(APIView):
    def get(self,request, *args, **kwargs):
        return Response("hello world")
# # 主页
# def index(request, ):
#     username = request.user
#     return render(request, 'login/index.html', locals())
#
#
# 登录


## 注册
# def register(request):
#     if request.method == 'POST' and request.POST:
#         data = request.POST
#         username = data.get("username")
#         password = data.get("password")
#         # 校验注册，名字不可重复
#         u = User.objects.filter(username=username).first()
#         if u:
#             info = '该用户名已被注册'
#             return render(request, 'login/ERROR.html', {'info': info})
#         else:
#             # 注册成功，创建用户
#             User.objects.create_user(
#                 username=username,
#                 password=password
#             )
#             # 重定向到登录页面
#             return HttpResponseRedirect('/tologin/')
#     # 注册失败，重新注册
#     return render(request, 'login/register.html')
#
#
# def lagout(request):
#     logout(request)
#     return redirect('/')