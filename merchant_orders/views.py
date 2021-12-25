import requests
from django.shortcuts import render
import pymysql
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
import json
from SQL_connection.sqlhelper import SqlHelper
# Create your views here.

class Orders(APIView):
    def get(self, request, *args, **kargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /merorder/orders")
            data = request.GET  # 处理请求
            mer_id = data.get('mer_id')
            print(mer_id)
            user = User.objects.filter(username=mer_id)
            if user is not None:
                user = User.objects.get(username=mer_id)
                if user.is_staff == 1:
                    obj = SqlHelper()
                    sql_select = 'select order_id, user_name, goods_name, image, num, amount, state ' \
                                 'from mall.view_merorder_orders ' \
                                 'where mer_id = %s'
                    result_list = obj.get_list(sql_select, [mer_id, ])
                    obj.close()
                    resp = {
                        'id': 0,
                        'msg': 'success',
                        'payload': result_list
                    }
                else:
                    resp = {
                        'id': -1,
                        'msg': "the merchant id doesn't exist"
                    }
            else:
                resp = {
                    'id': -1,
                    'msg': "the merchant id doesn't exist"
                }
            return Response(resp)


class OrderDetail(APIView):
    def get(self, request, *args, **kargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /merorder/orderdetail")
            data = request.GET
            obj = SqlHelper()
            order_id = data.get('order_id')
            sql_select2 = 'select add_time, user_name, mobile, address ' \
                          'from view_merorder_detail ' \
                          'where order_id = %s'
            result = obj.get_one(sql_select2, [order_id, ])
            obj.close()
            resp = {
                'id': 0,
                'msg': 'success',
                'payload': result
            }

            return Response(resp)
