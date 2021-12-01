
# Create your views here.
#from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#from django.contrib.auth import authenticate, login, logout
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

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status':True,
            'token': token.key,
            'user_id': user.pk,
            'user_name':user.username,
        })
# # 主页
# def index(request, ):
#     username = request.user
#     return render(request, 'LOGIN/index.html', locals())
#
#
# # 登录
# def tologin(request):
#     if request.method == 'POST' and request.POST:
#         data = request.POST
#         username = data.get('username')
#         password = data.get('password')
#         n = authenticate(username=username, password=password)
#         if n:
#             # 登陆成功即可获取当前登录用户，返回主页
#             login(request, user=n)
#             return redirect('/')
#     # 失败重定向到登录页
#     return render(request, 'LOGIN/login.html')
#
#
# # 注册
# def register(request):
#     if request.method == 'POST' and request.POST:
#         data = request.POST
#         username = data.get("username")
#         password = data.get("password")
#         # 校验注册，名字不可重复
#         u = User.objects.filter(username=username).first()
#         if u:
#             info = '该用户名已被注册'
#             return render(request, 'LOGIN/ERROR.html', {'info': info})
#         else:
#             # 注册成功，创建用户
#             User.objects.create_user(
#                 username=username,
#                 password=password
#             )
#             # 重定向到登录页面
#             return HttpResponseRedirect('/tologin/')
#     # 注册失败，重新注册
#     return render(request, 'LOGIN/register.html')
#
#
# def lagout(request):
#     logout(request)
#     return redirect('/')
