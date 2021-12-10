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
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /goods_search")
            data = request.GET
            goods_id = data.get('goods_id')
            mer_id = data.get('mer_id')

            print(goods_id)
            print(mer_id)
'''
            if mer_id.filter(username=user_id).exists():
                print("1")
                # inquiry_sql = 'select order_id,mer_id,goods_id,city,address from mall1.orderitem where user_id = %s'
                resp = {
                    'id': 0,
                    'msg': 'Success',
                    'payload': {
                        "order_id": "订单号",
                        "mer_name": "店铺名",
                        "goods_name": "商品名",
                        "image": "商品图片src",
                        "num": "购买数量",
                        "amount": "金额"
                    }
                }
                return Response(resp)

            #写到这儿了，表mergoods需要加上这些元素，这个表专门服务goodssearch最好

            #下面都不是
'''

class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response("困！")