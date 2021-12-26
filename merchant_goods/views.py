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



# 添加商品
class Add(APIView):
    def post(self, request, *args, **kargs):
        if request.method == 'POST':  # 要求使用POST请求方式
            print("receive POST request at /addgoods")
            data = json.loads(request.body)
            mer_id = data.get('mer_id')
            goods_id = data.get('goods_id')
            price = data.get('price')
            sales = data.get('sales')
            stock = data.get('stock')
            print(mer_id)
            print(goods_id)
            print(price)
            print(sales)
            print(stock)

            obj = SqlHelper()
            sql_check1 = 'select name ' \
                         'from mall.merchant ' \
                         'where mer_id = %s '
            check1 = obj.get_one(sql_check1, [mer_id,])
            print(check1)

            if check1 is not None:
                sql_addgoods = 'insert into mall.mergoods(mer_id, goods_id, price, stock, sales) ' \
                               'values(%s, %s, %s, %s, %s)'
                obj.modify(sql_addgoods, [mer_id, goods_id, price, stock, sales])
                obj.close()
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
            else:
                resp = {
                    'id': -1,
                    'msg': 'Fail'
                }
            return Response(resp)



# 删除商品
class Delete(APIView):
    def post(self, request, *args, **kargs):
        if request.method == 'POST':  # 要求使用POST请求方式
            print("receive POST request at /delete")
            data = json.loads(request.body)
            mer_id = data.get('mer_id')
            goods_id = data.get('goods_id')
            print(mer_id)
            print(goods_id)
            obj = SqlHelper()
            sql_check2 = 'select name ' \
                         'from mall.merchant ' \
                         'where mer_id = %s '
            check2 = obj.get_one(sql_check2, [mer_id, ])
            print(check2)

            if check2 is not None:
                sql_delete = 'update mall.mergoods ' \
                             'set state = 1 ' \
                             'where mer_id = %s ' \
                             'and goods_id = %s'
                obj.modify(sql_delete, [mer_id, goods_id])
                obj.close()
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
            else:
                resp = {
                    'id': -1,
                    'msg': 'Fail'
                }
            return Response(resp)


class Alter(APIView):
    def post(self, request, *args, **kargs):
        if request.method == 'POST':  # 要求使用POST请求方式
            print("receive POST request at /alter")
            data = json.loads(request.body)
            mer_id = data.get('mer_id')
            goods_id = data.get('goods_id')
            price = data.get('price')
            sales = data.get('sales')
            stock = data.get('stock')
            print(mer_id)
            print(goods_id)
            print(price)
            print(sales)
            print(stock)

            obj = SqlHelper()
            sql_check3 = 'select goods_id ' \
                         'from mall.mergoods ' \
                         'where mer_id = %s'
            check3 = obj.get_one(sql_check3, [mer_id,])
            print(check3)

            if check3 is not None:
                sql_alter = 'update mall.mergoods ' \
                            'set price = %s, sales = %s, stock = %s ' \
                            'where mer_id = %s ' \
                            'and goods_id = %s'
                obj.modify(sql_alter, [price, sales, stock, mer_id, goods_id, ])
                obj.close()
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
            else:
                resp = {
                    'id': -1,
                    'msg': 'Fail'
                }
            return Response(resp)






