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
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
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
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            obj = SqlHelper()
            sql_check2 = 'select name ' \
                         'from mall.merchant ' \
                         'where mer_id = %s '
            check2 = obj.get_one(sql_check2, [mer_id, ])
            print(check2)

            if check2 is not None:
                sql_delete = 'delete ' \
                             'from mall.mergoods ' \
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
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
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



# ####################################以下存疑#######################################


# 该商家的所有订单

# Those script write in old pattern.
# Now we're using new method with pymysql.

class Goods_Bill(APIView):
    def get(self, request, *args, **kargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /bill_of_goods")
            data = request.GET  # 处理请求
            mer_id = data.get('mer_id')
            print(mer_id)
            user = User.objects.filter(username=mer_id)
            if user is not None:
                user = User.objects.get(username=mer_id)
                if user.is_staff == 1:
                    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
                    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                    sql_select0 = "select goods_id,price,sales,stock " \
                                      "from mergoods " \
                                      "where mer_id = %s"
                    cursor.execute(sql_select0, [mer_id, ])
                    sql_select = "select goods.goods_id,goods.goods_name,goods.image,mergoods.price,mergoods.sales,mergoods.stock " \
                                 "from goods,mergoods " \
                                 "where goods.goods_id = mergoods.goods_id"
                    cursor.execute(sql_select)
                    result_list = cursor.fetchall()
                    conn.close()
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