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
from django.http import QueryDict


class UserView(View):

    def get(self, request):
        pass

    def delete(self, request):
        DELETE = QueryDict(request.body)
        name = DELETE.get('name')
        print(name)
        return JsonResponse({'code': 200, 'msg': 'success'}, safe=False)


# Create your views here.

class cart_inquiry(APIView):

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /cart_inquiry")
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

class carts_delete(APIView):
    def delete(self,request,*args,**kwargs):
        if request.method == 'DELETE':
            data = QueryDict(request.body)
            user_id = data.get('user_id')
            goods_id = int(data.get('goods_id'))
            mer_id = data.get('mer_id')
            sql_delete = "delete from mall.cart " \
                         "where goods_id =%s and mer_id = %s and user_id = %s"
            obj = SqlHelper()
            result = obj.create(sql_delete,[goods_id, mer_id, user_id, ])
            obj.close()
            if result:
                resp = {
                    'id': '0',
                    'msg': 'Success'
                }
                return Response(resp)
            else:
                resp = {
                    'id': '-1',
                    'msg': 'failure'
                }
                return Response(resp)
