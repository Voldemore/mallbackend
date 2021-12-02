
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


# Create your views here.
# 用户注册
class Register(APIView):
    def post(self,request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            resp = {
                'status':False,
                'data':'用户名已被注册'
            }
        else:
            user = User.objects.create_user(username=username,password=password)
            token, created = Token.objects.get_or_create(user=user)
            resp = {
                'status':True,
                'token': token.key,
                'user_id': user.pk,
                'user_name': user.username,
            }
        return Response(resp)

# 用户登录
class Login(APIView):
    def tologin(request):
        if request.method == 'POST' and request.POST:
            data = request.POST
            username = data.get('username')
            password = data.get('password')
            #   内置验证
            #   username = auth.authenticate(username = username, password = password)

            n = authenticate(username=username, password=password)
            if n:
                # 登陆成功即可获取当前登录用户，返回主页
                auth.login(request, user=n)
                return redirect('/login/')
        # 失败重定向到登录页
        return render(request, 'login.html')


class Test(APIView):
    def post(self,request, *args, **kwargs):
        return Response("hello world")
# # 主页
# def index(request, ):
#     username = request.user
#     return render(request, 'login/index.html', locals())
#
#
# 登录

#def index(request):


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