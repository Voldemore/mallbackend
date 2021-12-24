from django.shortcuts import render
import datetime
import pymysql
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.db import connection
import json
from SQL_connection.sqlhelper import SqlHelper


# Create your views here.

class cart_query(APIView):

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /merchant_info")
            data = request.GET  # 处理请求
            user_id = data.get('user_id')
            print(user_id)
            user = User.objects.filter(username=user_id)
            if user is not None:
                user = User.objects.get(username=user_id)
                if user.is_staff == 0:
                    obj = SqlHelper()
                    sql_select = 'select goods_id,mer_id,num,add_time,pic,goods_name,mer_name,price ' \
                                 'from mall.view_cart_users ' \
                                 'where user_id = %s'
                    result = obj.get_list(sql_select, [user_id, ])
                    obj.close()
                    resp = {
                        'id': 0,
                        'msg': 'success',
                        'payload': result
                    }
                else:
                    resp = {
                        'id': -1,
                        'msg': "the user id doesn't exist"
                    }
            else:
                resp = {
                    'id': -1,
                    'msg': "the user id doesn't exist"
                }
            return Response(resp)

#class
