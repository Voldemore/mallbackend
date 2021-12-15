from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.response import Response
from django.db import connection
import json
import pymysql
from SQL_connection.sqlhelper import SqlHelper


class MerQuery(APIView):
    []

class GoodsQuery(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /goods_search/goods_search")
            data = request.GET
            goods_name = data.get('goods_name')
            print(goods_name)

            # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            #
            # obj = SqlHelper()
            # sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
            #               'from mall.view_goods_search ' \
            #               'where mer_id = %s ' \
            #               'order by price'
            # result1 = obj.get_list(sql_select1, [mer_id, ])
            # result2 = obj.get_one(sql_select1, [mer_id, ])
            # print(result2)
            # if result2 is not None:
            #     obj.close()
            #     resp = {
            #         'id': 0,
            #         'msg': 'Success',
            #         'payload': result1
            #     }
            # else:
            #     resp = {
            #         'id': -1,
            #         'msg': 'Goods can not found',
            #         'payload': []
            #     }
            # return Response(resp)