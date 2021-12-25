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
from datetime import datetime


# Create your views here.
# 购物车查询
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
                                 'from mall.view_cart_users where user_id = %s order by add_time desc '
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


# 删除购物车
class carts_delete(APIView):
    def delete(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            data = json.loads(request.body)
            print(data)
            user_id = data.get('user_id')
            goods_id = int(data.get('goods_id'))
            mer_id = data.get('mer_id')
            sql_delete = "delete from mall.cart " \
                         "where goods_id =%s and mer_id = %s and user_id = %s"
            obj = SqlHelper()
            result = obj.create(sql_delete, [goods_id, mer_id, user_id, ])
            obj.close()
            print(result)
            resp = {
                'id': '0',
                'msg': 'Success'
            }
            return Response(resp)
            # else:
            #     resp = {
            #         'id': '-1',
            #         'msg': 'failure'
            #     }
            #     return Response(resp)


# 购物车生成订单
class Confirm_order(APIView):
    def post(self, request, *args, **kwargs):
        print("received the post request at api/carts/comfirm_order/")
        data = json.loads(request.body)  # 涉及到购物车，库存，订单那张表
        print(data)
        user_id = data.get('user_id')  # 购物车
        addr_id = int(data.get('addr_id'))  # 订单
        goods_id = int(data.get('goods_id'))  # 购物车  mergoods
        mer_id = data.get('mer_id')  # 购物车 mergoods
        num = int(data.get('num'))  # 购物车 mergoods
        amount = int(data.get('amount'))  # 订单表
        flag = 0  # 标志变量，如果生成订单成功则为0，若失败，则为1
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql_delete = "delete from mall.cart where goods_id = %s and mer_id = %s and user_id = %s"
            cursor.execute(sql_delete, [goods_id, mer_id, user_id, ])
            sql_update = "update mall.mergoods set stock = stock - %s,sales = sales+%s where mer_id = %s and goods_id= %s"
            cursor.execute(sql_update, [num, num, mer_id, goods_id, ])
            sql_insert = "insert into mall.orderitem(goods_id, mer_id, user_id, num, amount, add_time, addr_id) " \
                         "values (%s,%s,%s,%s,%s,%s,%s)"
            add_time = datetime.now()
            cursor.execute(sql_insert, [goods_id, mer_id, user_id, num, amount, add_time, addr_id, ])
            conn.commit()  # 事务提交
        except Exception as e:
            conn.rollback()  # 事务回滚
            flag = 1
        finally:
            # 5.释放资源
            cursor.close()
            conn.close()
        if flag == 0:
            resp = {
                "id": 0,
                "msg": "Success"
            }
        if flag == 1:
            resp = {
                "id": -1,
                "msg": "failure"
            }
        return Response(resp)
