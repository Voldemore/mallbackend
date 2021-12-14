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
            variety = data.get('keywords')
            order = data.get('order')
            direction = data.get('direction')       #默认升序
            print(variety)
            print(order)
            print(direction)

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            if order=="价格":

                if direction=="升序":
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where variety = %s ' \
                                  'order by price'
                    result1 = obj.get_list(sql_select1, [variety, ])
                    obj.close()
                    resp = {
                        'id': 0,
                        'msg': 'Success',
                        'payload': result1
                    }
                    return Response(resp)

                elif direction == "降序":
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where variety = %s ' \
                                  'order by price desc'
                    result1 = obj.get_list(sql_select1, [variety, ])
                    obj.close()
                    resp = {
                        'id': 0,
                        'msg': 'Success',
                        'payload': result1
                    }
                    return Response(resp)





# class MerchantSearch(APIView):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             print("receive POST request at /goods_search/merchant_search")
#             data = request.GET
#             variety = data.get('keywords')
#
#             print(variety)

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

class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response("困！")
