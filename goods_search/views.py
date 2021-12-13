from django.shortcuts import render

# Create your views here.
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.response import Response
from django.db import connection
import json
import pymysql
from SQL_connection.sqlhelper import SqlHelper


class GoodsSearch(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive POST request at /goods_search/goods_search")
            data = request.GET
            variety = data.get('variety')
            print(variety)

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            obj = SqlHelper()
            sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                          'from mall.view_goods_search ' \
                          'where variety = %s '
            result1 = obj.get_list(sql_select1, [variety, ])
            obj.close()
            resp = {
                'id': 0,
                'msg': 'Success',
                'payload': result1
            }
            return Response(resp)


# class GoodsSearch(APIView):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             print("receive GET request at /goods_search/goods_search")
#             data = json.loads(request.body)
#             variety = data.get('variety')
#
#             print(variety)
#
#             operation_select = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
#                                'from mall.view_goods_search ' \
#                                'where type = %s '
#             cursor = connection.cursor()
#             cursor.execute(operation_select, [variety])
#             result = cursor.fetchall()
#
#             dict_res = {
#                 'time': datetime.datetime.now(),
#                 'goods_id': result[0],
#                 'maker': result[1],
#                 'image': result[2],
#                 'goods_name': result[3]
#             }
#
#             resp = {
#                 'id': 0,
#                 'msg': 'Success',
#                 'payload': dict_res
#             }
#
#             return Response(resp)


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
