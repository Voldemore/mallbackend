from django.shortcuts import render

# Create your views here.
import datetime

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
#from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.db import connection
import json


class GoodsSearch(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /goods_search")
            data = json.loads(request.body)
            goods_id = data.get('goods_id')
            mer_id = data.get('mer_id')

        n = authenticate(goods_id=goods_id, mer_id=mer_id)
        print(n)
        if n is not None:
            # 登陆成功即可获取当前登录用户，返回主页
            auth.login(request, user=n)
            operation_select = 'select goods_name,mer_name,goods_image,price,sales,description,comments,stock from mergoods where goods_id = %s and mer_id = %s'

            #写到这儿了，表mergoods需要加上这些元素，这个表专门服务goodssearch最好

            #下面都不是


class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response("困！")