from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django.db import connection
import json
from rest_framework.authtoken.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from SQL_connection.sqlhelper import SqlHelper
import pymysql

class order_inquiry(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':#要求使用GET请求方式
            print("receive GET request at /order_inquiry")

            data = request.GET#处理请求
            user_id = data.get('user_id')
            print(user_id)
            if User.objects.filter(username=user_id).exists():
                user = User.objects.get(username=user_id)

                if user.is_staff == 0:
                    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall1')
                    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

                    sql_create_view = "create view View_order(order_id,mer_id,goods_id,num,amount,state,add_time) as select order_id,mer_id,goods_id,num,amount,state,add_time from mall.orderitem where user_id = %s"
                    cursor.execute(sql_create_view,[user_id,])
                    sql_select = "select View_order.order_id,merchant_info.mer_name,goods_info.goods_name,goods_info.image,View_order.num,View_order.amount,View_order.state,View_order.add_time from mall.View_order View_order,mall.View_merchant_info merchant_info,mall.View_goods_info goods_info where View_order.goods_id = goods_info.goods_id and View_order.mer_id = merchant_info.mer_id"
                    cursor.execute(sql_select)
                    result_list = cursor.fetchall()
                    sql_drop_view = "drop view mall.View_order"
                    cursor.execute(sql_drop_view)
                    cursor.close()
                    conn.close()
                    resp = {
                            'id': 0,
                            'msg': 'Success',
                            'payload': result_list
                        }
                else:
                    resp = {
                        'id': -1,
                        'msg': "username doesn't exist",
                    }
            else:
                resp = {
                    'id': -1,
                    'msg': "username doesn't exist",
                }
            return Response(resp)

class order_details(APIView):
    def get(self,request,*args, **kwargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /order_inquiry")

            data = request.GET  # 处理请求
            order_id = int(data.get('user_id'))
            print(order_id)
            sql_select1 = 'select add_time,comments,addr_id from mall.orderitem where order_id = %s'
            obj = SqlHelper()
            result1 = obj.get_one(sql_select1,[order_id, ])
            address_id = result1['addr_id']
            if address_id is not None:
                sql_select2 = "select name,mobile,province,city,county,address from mall.address where addr_id = %s"
                result2 = obj.get_one(sql_select2, [address_id, ])
                obj.close()
                result1['name'] = result2['name']
                result1['mobile'] = result2['mobile']
                result1['province'] = result2['province']
                result1['county'] = result2['county']
                result1['address'] = result2['address']
                resp = {
                    'id': '0',
                    'msg': 'success',
                    'payload': result1
                }
            else:
                resp = {
                    'id': -1,
                    'msg': "The order_id doesn't exist"
                }
            return Response(resp)



